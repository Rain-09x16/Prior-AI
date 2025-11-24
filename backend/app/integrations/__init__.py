"""Integration modules."""
from app.integrations.google_patents import GooglePatentsAPI
from app.integrations.watsonx_nlu import WatsonxNLU
from app.integrations.watsonx_ai import WatsonxAI

__all__ = ["GooglePatentsAPI", "WatsonxNLU", "WatsonxAI"]
