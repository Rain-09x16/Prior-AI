"""Analysis API endpoints."""
from typing import Optional, List
import uuid
import json
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import Analysis, Patent
from app.schemas import AnalysisResponse, AnalysisListResponse, ExtractedClaims, PatentMatch
from app.services import DocumentParser, OrchestrateConductor, ReportGenerator
from app.utils import FileHandler
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/", response_model=AnalysisResponse, status_code=202)
async def create_analysis(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Create new analysis by uploading disclosure document.

    Args:
        file: PDF or DOCX file
        title: Optional title for the analysis
        db: Database session

    Returns:
        Analysis response with processing status
    """
    logger.info(f"Received file upload: {file.filename}")

    # Validate file
    file_handler = FileHandler()
    file_handler.validate_file(file)

    try:
        # Save file to disk
        original_filename, file_path = await file_handler.save_file(
            file,
            settings.DISCLOSURES_DIR
        )
        logger.info(f"Saved file to: {file_path}")

        # Determine title
        if not title:
            title = FileHandler.get_file_type(original_filename)
            parser = DocumentParser()
            try:
                text = parser.parse(file_path, FileHandler.get_file_type(original_filename))
                title = parser.extract_title(text, original_filename)
            except:
                title = original_filename

        # Create analysis record
        analysis = Analysis(
            uuid=str(uuid.uuid4()),
            title=title,
            status="processing",
            disclosure_filename=original_filename,
            disclosure_path=file_path
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        logger.info(f"Created analysis record: {analysis.id} (UUID: {analysis.uuid})")

        # Trigger background analysis
        background_tasks.add_task(
            run_analysis_workflow,
            analysis.id,
            file_path,
            FileHandler.get_file_type(original_filename),
            db
        )

        # Return response
        return AnalysisResponse(
            id=analysis.uuid,
            title=analysis.title,
            status=analysis.status,
            disclosure={
                "filename": analysis.disclosure_filename,
                "uploadedAt": analysis.created_at
            },
            createdAt=analysis.created_at
        )

    except Exception as e:
        logger.error(f"Failed to create analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create analysis: {str(e)}")


async def run_analysis_workflow(
    analysis_id: int,
    file_path: str,
    file_type: str,
    db: Session
):
    """
    Background task to run the complete analysis workflow.

    Args:
        analysis_id: Database ID of the analysis
        file_path: Path to the uploaded file
        file_type: Type of file (pdf or docx)
        db: Database session
    """
    logger.info(f"Starting background analysis workflow for analysis_id={analysis_id}")

    # Get fresh database session for background task
    from app.database import SessionLocal
    db = SessionLocal()

    try:
        # Get analysis record
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            logger.error(f"Analysis not found: {analysis_id}")
            return

        # Step 1: Parse document
        logger.info("Step 1: Parsing document...")
        parser = DocumentParser()
        document_text = parser.parse(file_path, file_type)
        logger.info(f"Parsed {len(document_text)} characters from document")

        # Step 2: Run orchestration
        logger.info("Step 2: Running orchestration workflow...")
        conductor = OrchestrateConductor(db)
        results = await conductor.run_analysis(analysis_id, document_text)

        # Step 3: Save results to database
        logger.info("Step 3: Saving results to database...")

        # Save extracted claims
        analysis.extracted_claims = json.dumps(results.get('extractedClaims'))

        # Save patents
        for patent_data in results.get('patents', [])[:20]:  # Save top 20
            patent = Patent(
                analysis_id=analysis_id,
                patent_id=patent_data.get('patentId', ''),
                title=patent_data.get('title', ''),
                abstract=patent_data.get('abstract', ''),
                claims=json.dumps(patent_data.get('claims', [])),
                publication_date=patent_data.get('publicationDate'),
                assignee=patent_data.get('assignee', ''),
                inventors=json.dumps(patent_data.get('inventors', [])),
                ipc_classifications=json.dumps(patent_data.get('ipcClassifications', [])),
                similarity_score=patent_data.get('similarityScore', 0.0),
                overlapping_concepts=json.dumps(patent_data.get('overlappingConcepts', [])),
                key_differences=json.dumps(patent_data.get('keyDifferences', [])),
                source=patent_data.get('source', 'google')
            )
            db.add(patent)

        # Save recommendation
        analysis.novelty_score = results.get('noveltyScore')
        analysis.recommendation = results.get('recommendation')
        analysis.reasoning = results.get('reasoning')
        analysis.status = "completed"
        analysis.completed_at = datetime.utcnow()

        db.commit()
        logger.info(f"Analysis completed successfully: {analysis.uuid}")

    except Exception as e:
        logger.error(f"Analysis workflow failed: {str(e)}")
        # Update analysis status to failed
        try:
            analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.status = "failed"
                analysis.reasoning = f"Analysis failed: {str(e)}"
                db.commit()
        except Exception as db_error:
            logger.error(f"Failed to update analysis status: {str(db_error)}")

    finally:
        db.close()


@router.get("/{analysis_uuid}", response_model=AnalysisResponse)
async def get_analysis(analysis_uuid: str, db: Session = Depends(get_db)):
    """
    Get analysis by UUID.

    Args:
        analysis_uuid: UUID of the analysis
        db: Database session

    Returns:
        Analysis response
    """
    logger.info(f"Fetching analysis: {analysis_uuid}")

    # Get analysis
    analysis = db.query(Analysis).filter(Analysis.uuid == analysis_uuid).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    # Parse extracted claims
    extracted_claims = None
    if analysis.extracted_claims:
        try:
            claims_data = json.loads(analysis.extracted_claims)
            extracted_claims = ExtractedClaims(**claims_data)
        except Exception as e:
            logger.error(f"Failed to parse claims: {str(e)}")

    # Get patents
    patents_data = []
    patents = db.query(Patent).filter(Patent.analysis_id == analysis.id).order_by(desc(Patent.similarity_score)).all()
    for patent in patents:
        try:
            patent_dict = {
                "id": str(patent.id),
                "patentId": patent.patent_id,
                "title": patent.title,
                "abstract": patent.abstract,
                "claims": json.loads(patent.claims) if patent.claims else [],
                "publicationDate": patent.publication_date.isoformat() if patent.publication_date else None,
                "assignee": patent.assignee,
                "inventors": json.loads(patent.inventors) if patent.inventors else [],
                "ipcClassifications": json.loads(patent.ipc_classifications) if patent.ipc_classifications else [],
                "similarityScore": patent.similarity_score,
                "overlappingConcepts": json.loads(patent.overlapping_concepts) if patent.overlapping_concepts else [],
                "keyDifferences": json.loads(patent.key_differences) if patent.key_differences else [],
                "source": patent.source
            }
            patents_data.append(PatentMatch(**patent_dict))
        except Exception as e:
            logger.error(f"Failed to parse patent {patent.id}: {str(e)}")

    # Build response
    return AnalysisResponse(
        id=analysis.uuid,
        title=analysis.title,
        status=analysis.status,
        disclosure={
            "filename": analysis.disclosure_filename,
            "uploadedAt": analysis.created_at
        },
        extractedClaims=extracted_claims,
        patents=patents_data,
        noveltyScore=analysis.novelty_score,
        recommendation=analysis.recommendation,
        reasoning=analysis.reasoning,
        createdAt=analysis.created_at,
        updatedAt=analysis.updated_at,
        completedAt=analysis.completed_at
    )


@router.get("/", response_model=AnalysisListResponse)
async def list_analyses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    List all analyses with pagination.

    Args:
        page: Page number (starts at 1)
        limit: Items per page
        status: Filter by status
        db: Database session

    Returns:
        List of analyses with pagination info
    """
    logger.info(f"Listing analyses: page={page}, limit={limit}, status={status}")

    # Build query
    query = db.query(Analysis)

    # Filter by status if provided
    if status:
        query = query.filter(Analysis.status == status)

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    analyses = query.order_by(desc(Analysis.created_at)).offset(offset).limit(limit).all()

    # Build response
    data = []
    for analysis in analyses:
        data.append(AnalysisResponse(
            id=analysis.uuid,
            title=analysis.title,
            status=analysis.status,
            disclosure={
                "filename": analysis.disclosure_filename,
                "uploadedAt": analysis.created_at
            },
            noveltyScore=analysis.novelty_score,
            recommendation=analysis.recommendation,
            createdAt=analysis.created_at,
            updatedAt=analysis.updated_at,
            completedAt=analysis.completed_at
        ))

    return AnalysisListResponse(
        data=data,
        total=total,
        page=page,
        limit=limit,
        pages=(total + limit - 1) // limit
    )


@router.post("/{analysis_uuid}/report")
async def generate_report(analysis_uuid: str, db: Session = Depends(get_db)):
    """
    Generate PDF report for analysis.

    Args:
        analysis_uuid: UUID of the analysis
        db: Database session

    Returns:
        Report URL and expiration
    """
    logger.info(f"Generating report for analysis: {analysis_uuid}")

    # Get analysis
    analysis = db.query(Analysis).filter(Analysis.uuid == analysis_uuid).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if analysis.status != "completed":
        raise HTTPException(status_code=400, detail="Analysis not completed yet")

    try:
        # Get full analysis data
        analysis_data = await get_analysis(analysis_uuid, db)

        # Convert to dict for report generator
        analysis_dict = {
            "id": analysis_data.id,
            "title": analysis_data.title,
            "status": analysis_data.status,
            "createdAt": analysis_data.createdAt.isoformat() if analysis_data.createdAt else None,
            "extractedClaims": analysis_data.extractedClaims.dict() if analysis_data.extractedClaims else None,
            "patents": [p.dict() for p in analysis_data.patents] if analysis_data.patents else [],
            "noveltyScore": analysis_data.noveltyScore,
            "recommendation": analysis_data.recommendation,
            "reasoning": analysis_data.reasoning
        }

        # Generate report
        report_filename = f"{analysis_uuid}.pdf"
        report_path = str(settings.REPORTS_DIR / report_filename)

        generator = ReportGenerator()
        generator.generate(analysis_dict, report_path)

        return {
            "reportUrl": f"/api/v1/reports/{report_filename}",
            "expiresAt": None  # No expiration for hackathon
        }

    except Exception as e:
        logger.error(f"Failed to generate report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.delete("/{analysis_uuid}", status_code=204)
async def delete_analysis(analysis_uuid: str, db: Session = Depends(get_db)):
    """
    Delete analysis and associated data.

    Args:
        analysis_uuid: UUID of the analysis
        db: Database session
    """
    logger.info(f"Deleting analysis: {analysis_uuid}")

    # Get analysis
    analysis = db.query(Analysis).filter(Analysis.uuid == analysis_uuid).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    try:
        # Delete associated files
        FileHandler.delete_file(analysis.disclosure_path)

        # Delete from database (cascade will delete patents and logs)
        db.delete(analysis)
        db.commit()

        logger.info(f"Deleted analysis: {analysis_uuid}")

    except Exception as e:
        logger.error(f"Failed to delete analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete analysis: {str(e)}")


@router.get("/reports/{filename}")
async def download_report(filename: str):
    """
    Download generated PDF report.

    Args:
        filename: Report filename

    Returns:
        PDF file
    """
    report_path = settings.REPORTS_DIR / filename

    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        path=str(report_path),
        media_type="application/pdf",
        filename=filename
    )
