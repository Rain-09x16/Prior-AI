"""
PDF Report Generator for prior art analysis.
"""
from typing import Dict, List
import json
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ReportGenerator:
    """Generate PDF reports for prior art analysis."""

    def __init__(self):
        """Initialize the report generator."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        logger.info("Initialized Report Generator")

    def _setup_custom_styles(self):
        """Set up custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        # Subsection heading style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))

        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=14
        ))

    def generate(self, analysis: Dict, output_path: str) -> str:
        """
        Generate PDF report for analysis.

        Args:
            analysis: Analysis data dictionary
            output_path: Path to save the PDF report

        Returns:
            Path to generated PDF file
        """
        logger.info(f"Generating PDF report: {output_path}")

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Build content elements
        elements = []

        # Title Page
        elements.extend(self._build_title_page(analysis))
        elements.append(PageBreak())

        # Executive Summary
        elements.extend(self._build_executive_summary(analysis))
        elements.append(Spacer(1, 0.2 * inch))

        # NEW v2.1: Patentability Assessment Section
        if analysis.get('isPatentable') is not None:
            elements.extend(self._build_patentability_section(analysis))
            elements.append(Spacer(1, 0.2 * inch))

        # Extracted Claims
        elements.extend(self._build_claims_section(analysis))
        elements.append(Spacer(1, 0.2 * inch))

        # Patent Analysis
        elements.extend(self._build_patents_section(analysis))
        elements.append(PageBreak())

        # Recommendation
        elements.extend(self._build_recommendation_section(analysis))

        # Appendix
        elements.extend(self._build_appendix(analysis))

        # Build PDF
        try:
            doc.build(elements)
            logger.info(f"Successfully generated PDF report: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to generate PDF: {str(e)}")
            raise Exception(f"PDF generation failed: {str(e)}")

    def _build_title_page(self, analysis: Dict) -> List:
        """Build title page elements."""
        elements = []

        # Title
        elements.append(Spacer(1, 2 * inch))
        title = Paragraph("Prior Art Analysis Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5 * inch))

        # Disclosure title
        disclosure_title = Paragraph(
            f"<b>{analysis.get('title', 'Untitled Disclosure')}</b>",
            self.styles['Heading2']
        )
        elements.append(disclosure_title)
        elements.append(Spacer(1, 1 * inch))

        # Metadata table
        created_at = analysis.get('createdAt', '')
        if created_at:
            try:
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00')).strftime('%B %d, %Y')
            except:
                pass

        metadata = [
            ['Analysis ID:', analysis.get('id', 'N/A')],
            ['Generated:', created_at],
            ['Status:', analysis.get('status', 'N/A').title()],
            ['Recommendation:', (analysis.get('recommendation', 'N/A').upper())],
        ]

        t = Table(metadata, colWidths=[2 * inch, 4 * inch])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(t)

        return elements

    def _build_executive_summary(self, analysis: Dict) -> List:
        """Build executive summary section."""
        elements = []

        elements.append(Paragraph("Executive Summary", self.styles['SectionHeading']))

        # NEW v2.1: Include patentability assessment in summary
        is_patentable = analysis.get('isPatentable')
        patentability_confidence = analysis.get('patentabilityConfidence')
        novelty_score = analysis.get('noveltyScore', 0)
        recommendation = analysis.get('recommendation', 'N/A')

        # Different summary based on patentability
        if is_patentable is False:
            summary_text = f"""
            <b>IMPORTANT: Patentability Assessment indicates this disclosure is NOT patentable.</b><br/><br/>
            This disclosure was assessed for patentability before conducting the expensive prior art search.
            The initial assessment (confidence: {patentability_confidence:.1f}%) determined that the disclosure
            appears to be publishable research but lacks key elements required for patent protection.
            As a result, the prior art search was skipped, saving approximately $500-$1,000 in search costs.<br/><br/>
            Please review the patentability assessment section for specific recommendations on how to revise
            the disclosure to make it patentable, or consider publishing as academic research instead.
            """
        elif is_patentable is True:
            summary_text = f"""
            This report presents the results of a comprehensive prior art analysis for the submitted invention disclosure.
            The disclosure passed the initial patentability assessment (confidence: {patentability_confidence:.1f}%),
            indicating it contains the necessary elements for patent protection. The analysis then identified and
            evaluated similar patents to assess the novelty and patentability of the invention.
            """
        else:
            summary_text = f"""
            This report presents the results of a comprehensive prior art analysis for the submitted invention disclosure.
            The analysis identified and evaluated similar patents to assess the novelty and patentability of the invention.
            """

        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.1 * inch))

        # Score summary table
        score_color = self._get_score_color(novelty_score)
        rec_color = self._get_recommendation_color(recommendation)

        summary_data = [
            ['Metric', 'Value', 'Assessment'],
            ['Novelty Score', f'{novelty_score:.1f}/100', self._get_novelty_assessment(novelty_score)],
            ['Recommendation', recommendation.upper(), self._get_recommendation_text(recommendation)],
            ['Patents Analyzed', str(len(analysis.get('patents', []))), 'Similar patents found'],
        ]

        t = Table(summary_data, colWidths=[1.8 * inch, 1.5 * inch, 3.2 * inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(t)

        return elements

    def _build_patentability_section(self, analysis: Dict) -> List:
        """Build patentability assessment section (NEW in v2.1)."""
        elements = []

        elements.append(Paragraph("Patentability Assessment", self.styles['SectionHeading']))

        is_patentable = analysis.get('isPatentable')
        confidence = analysis.get('patentabilityConfidence', 0)
        missing_elements_str = analysis.get('missingElements', '[]')

        # Parse missing elements if JSON string
        try:
            missing_elements = json.loads(missing_elements_str) if isinstance(missing_elements_str, str) else []
        except:
            missing_elements = []

        # Assessment overview
        if is_patentable:
            assessment_text = f"""
            <b>Result: PATENTABLE</b> (Confidence: {confidence:.1f}%)<br/><br/>
            This disclosure passed the initial patentability screening and contains the necessary elements
            for patent protection. The analysis proceeded with a comprehensive prior art search.
            """
            text_color = colors.green
        else:
            assessment_text = f"""
            <b>Result: NOT PATENTABLE</b> (Confidence: {confidence:.1f}%)<br/><br/>
            This disclosure did not pass the initial patentability screening. The disclosure appears to be
            publishable research but lacks key elements required for patent protection. The expensive prior
            art search was skipped to save costs (approximately $500-$1,000).
            """
            text_color = colors.red

        elements.append(Paragraph(assessment_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.1 * inch))

        # Missing Elements (if any)
        if missing_elements and len(missing_elements) > 0:
            elements.append(Paragraph("Missing Elements for Patentability:", self.styles['SubsectionHeading']))

            for element in missing_elements:
                bullet = Paragraph(f"• {element}", self.styles['CustomBody'])
                elements.append(bullet)

            elements.append(Spacer(1, 0.1 * inch))

        # Value proposition box
        if not is_patentable:
            value_data = [
                ['Cost Savings', '$500 - $1,000'],
                ['Search Time Saved', '2-4 hours'],
                ['Early Feedback', 'Allows revision or publication'],
            ]

            elements.append(Paragraph("Value of Early Assessment:", self.styles['SubsectionHeading']))
            t = Table(value_data, colWidths=[3 * inch, 2 * inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fbbf24')),
            ]))
            elements.append(t)

        return elements

    def _build_claims_section(self, analysis: Dict) -> List:
        """Build extracted claims section."""
        elements = []

        elements.append(Paragraph("Extracted Claims", self.styles['SectionHeading']))

        claims = analysis.get('extractedClaims')
        if not claims:
            elements.append(Paragraph("No claims data available.", self.styles['CustomBody']))
            return elements

        # Parse claims if JSON string
        if isinstance(claims, str):
            try:
                claims = json.loads(claims)
            except:
                elements.append(Paragraph("Claims data format error.", self.styles['CustomBody']))
                return elements

        # Background
        if claims.get('background'):
            elements.append(Paragraph("Background", self.styles['SubsectionHeading']))
            elements.append(Paragraph(claims['background'][:500], self.styles['CustomBody']))
            elements.append(Spacer(1, 0.1 * inch))

        # Key Innovations
        if claims.get('innovations'):
            elements.append(Paragraph("Key Innovations", self.styles['SubsectionHeading']))
            for i, innovation in enumerate(claims['innovations'][:5], 1):
                elements.append(Paragraph(f"<b>{i}.</b> {innovation}", self.styles['CustomBody']))

        # Keywords
        if claims.get('keywords'):
            elements.append(Paragraph("Keywords", self.styles['SubsectionHeading']))
            keywords_text = ", ".join(claims['keywords'][:15])
            elements.append(Paragraph(keywords_text, self.styles['CustomBody']))

        # IPC Classifications
        if claims.get('ipcClassifications'):
            elements.append(Paragraph("IPC Classifications", self.styles['SubsectionHeading']))
            ipc_text = ", ".join(claims['ipcClassifications'])
            elements.append(Paragraph(ipc_text, self.styles['CustomBody']))

        return elements

    def _build_patents_section(self, analysis: Dict) -> List:
        """Build patents analysis section."""
        elements = []

        elements.append(Paragraph("Patent Analysis", self.styles['SectionHeading']))

        patents = analysis.get('patents', [])
        if not patents:
            elements.append(Paragraph("No patents found.", self.styles['CustomBody']))
            return elements

        # Top 10 most similar patents
        top_patents = patents[:10]

        elements.append(Paragraph(
            f"The analysis identified {len(patents)} relevant patents. "
            f"Below are the top {len(top_patents)} most similar patents:",
            self.styles['CustomBody']
        ))
        elements.append(Spacer(1, 0.2 * inch))

        for i, patent in enumerate(top_patents, 1):
            # Parse patent if needed
            if isinstance(patent, str):
                try:
                    patent = json.loads(patent)
                except:
                    continue

            elements.append(Paragraph(f"Patent {i}: {patent.get('patentId', 'N/A')}", self.styles['SubsectionHeading']))

            patent_data = [
                ['Title:', patent.get('title', 'N/A')],
                ['Similarity Score:', f"{patent.get('similarityScore', 0):.1f}%"],
                ['Publication Date:', patent.get('publicationDate', 'N/A')],
                ['Assignee:', patent.get('assignee', 'N/A')],
            ]

            t = Table(patent_data, colWidths=[1.5 * inch, 5 * inch])
            t.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(t)

            # Abstract
            if patent.get('abstract'):
                elements.append(Paragraph("<b>Abstract:</b>", self.styles['CustomBody']))
                abstract_text = patent['abstract'][:400] + "..." if len(patent.get('abstract', '')) > 400 else patent.get('abstract', '')
                elements.append(Paragraph(abstract_text, self.styles['CustomBody']))

            elements.append(Spacer(1, 0.15 * inch))

        return elements

    def _build_recommendation_section(self, analysis: Dict) -> List:
        """Build recommendation section."""
        elements = []

        elements.append(Paragraph("Recommendation", self.styles['SectionHeading']))

        recommendation = analysis.get('recommendation', 'N/A')
        reasoning = analysis.get('reasoning', 'No reasoning provided.')
        novelty_score = analysis.get('noveltyScore', 0)

        # Recommendation box
        rec_text = f"""
        <b>Recommendation: {recommendation.upper()}</b><br/>
        <b>Novelty Score: {novelty_score:.1f}/100</b><br/><br/>
        {reasoning}
        """

        rec_para = Paragraph(rec_text, self.styles['CustomBody'])
        elements.append(rec_para)

        return elements

    def _build_appendix(self, analysis: Dict) -> List:
        """Build appendix section."""
        elements = []

        elements.append(PageBreak())
        elements.append(Paragraph("Appendix", self.styles['SectionHeading']))

        appendix_text = """
        This report was generated by the Auto-Prior Art Analyst system using AI-powered analysis.
        The system analyzed the disclosure, searched patent databases, and evaluated similarity using
        advanced natural language processing and machine learning techniques.
        """

        elements.append(Paragraph(appendix_text, self.styles['CustomBody']))

        return elements

    def _get_score_color(self, score: float) -> colors.Color:
        """Get color based on score."""
        if score >= 70:
            return colors.green
        elif score >= 40:
            return colors.orange
        else:
            return colors.red

    def _get_recommendation_color(self, recommendation: str) -> colors.Color:
        """Get color based on recommendation."""
        if recommendation == 'pursue':
            return colors.green
        elif recommendation == 'reconsider':
            return colors.orange
        else:
            return colors.red

    def _get_novelty_assessment(self, score: float) -> str:
        """Get novelty assessment text."""
        if score >= 70:
            return "High novelty"
        elif score >= 40:
            return "Medium novelty"
        else:
            return "Low novelty"

    def _get_recommendation_text(self, recommendation: str) -> str:
        """Get recommendation description."""
        descriptions = {
            'pursue': 'Pursue patent protection',
            'reconsider': 'Reconsider with narrow claims',
            'reject': 'Not recommended for patenting'
        }
        return descriptions.get(recommendation, 'Unknown')
