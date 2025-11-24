"""
Patent searcher service for finding relevant prior art.
"""
from typing import List, Dict
from app.integrations.google_patents import GooglePatentsAPI
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class PatentSearcher:
    """Search patent databases for relevant prior art."""

    def __init__(self):
        """Initialize the patent searcher."""
        self.google_api = GooglePatentsAPI()
        logger.info("Initialized Patent Searcher")

    def search(
        self,
        keywords: List[str],
        ipc_codes: List[str],
        max_results: int = 100
    ) -> List[Dict]:
        """
        Search patents using keywords and IPC codes.

        Args:
            keywords: List of keywords to search for
            ipc_codes: List of IPC classification codes
            max_results: Maximum number of results to return

        Returns:
            List of formatted patent dictionaries
        """
        logger.info(f"Searching patents with {len(keywords)} keywords and {len(ipc_codes)} IPC codes")

        # Build search query
        query = self._build_query(keywords, ipc_codes)
        logger.info(f"Search query: {query}")

        # Search using Google Patents API
        patents = self.google_api.search(query, max_results)

        # Format results
        formatted_patents = []
        for patent in patents:
            formatted = self._format_patent(patent)
            formatted_patents.append(formatted)

        logger.info(f"Found and formatted {len(formatted_patents)} patents")
        return formatted_patents

    def _build_query(self, keywords: List[str], ipc_codes: List[str]) -> str:
        """
        Build search query from keywords and IPC codes.

        Args:
            keywords: List of keywords
            ipc_codes: List of IPC codes

        Returns:
            Query string
        """
        # Use top 5 keywords for search
        top_keywords = keywords[:5] if keywords else []

        # Build keyword query
        if top_keywords:
            keyword_query = " OR ".join(top_keywords)
        else:
            keyword_query = ""

        # Build IPC query
        if ipc_codes:
            ipc_query = " OR ".join([f"IPC:{code}" for code in ipc_codes])
        else:
            ipc_query = ""

        # Combine queries
        if keyword_query and ipc_query:
            return f"({keyword_query}) AND ({ipc_query})"
        elif keyword_query:
            return keyword_query
        elif ipc_query:
            return ipc_query
        else:
            return "technology"  # Fallback query

    def _format_patent(self, patent: Dict) -> Dict:
        """
        Format patent data to standard structure.

        Args:
            patent: Raw patent data from API

        Returns:
            Formatted patent dictionary
        """
        return {
            'patentId': patent.get('publication_number', ''),
            'title': patent.get('title', ''),
            'abstract': patent.get('abstract', ''),
            'claims': patent.get('claims', []),
            'publicationDate': patent.get('publication_date', ''),
            'assignee': patent.get('assignee', ''),
            'inventors': patent.get('inventors', []),
            'ipcClassifications': patent.get('ipc_classes', []),
            'source': patent.get('source', 'google')
        }

    def search_by_patent_id(self, patent_id: str) -> Dict:
        """
        Search for a specific patent by ID.

        Args:
            patent_id: Patent publication number

        Returns:
            Patent details dictionary
        """
        logger.info(f"Searching for patent: {patent_id}")
        patent = self.google_api.get_patent_details(patent_id)

        if patent:
            return self._format_patent(patent)
        else:
            logger.warning(f"Patent not found: {patent_id}")
            return {}
