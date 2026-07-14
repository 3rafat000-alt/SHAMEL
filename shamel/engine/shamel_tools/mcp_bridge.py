"""
role: shared library (shamel_tools)
purpose: re-export BrainMCPClient from brain_client for backward compat
gate: 0-8
"""
from .brain_client import BrainClient as BrainMCPClient

__all__ = ["BrainMCPClient"]
