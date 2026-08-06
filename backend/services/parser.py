"""
Scilab Output Parser service.

Parses raw console output streams, identifying progress indicators, warnings,
errors, execution metadata, and prompt signals.
"""

from dataclasses import dataclass
import re
from typing import Optional


@dataclass
class ParsedOutputLine:
    """DTO representing parsed output metadata."""
    raw_text: str
    line_type: str  # 'stdout', 'stderr', 'warning', 'error', 'progress', 'prompt'
    progress_percent: Optional[float] = None
    clean_text: str = ""


class ScilabOutputParser:
    """
    Parser for Scilab CLI stream output.
    """

    PROGRESS_REGEX = re.compile(r"\[\s*(\d+(?:\.\d+)?)\s*%\s*\]")
    WARNING_REGEX = re.compile(r"^warning\s*:", re.IGNORECASE)
    ERROR_REGEX = re.compile(r"^(?:error|!----\s*error)\s*:", re.IGNORECASE)

    def parse_line(self, line: str, is_stderr: bool = False) -> ParsedOutputLine:
        """
        Parse a single output line from Scilab.
        
        Args:
            line: Text line string.
            is_stderr: True if stream source is stderr.
            
        Returns:
            ParsedOutputLine DTO.
        """
        stripped = line.strip()

        # Check Progress pattern
        prog_match = self.PROGRESS_REGEX.search(line)
        if prog_match:
            try:
                percent = float(prog_match.group(1))
                return ParsedOutputLine(
                    raw_text=line,
                    line_type="progress",
                    progress_percent=percent,
                    clean_text=stripped,
                )
            except ValueError:
                pass

        # Check Error pattern
        if is_stderr or self.ERROR_REGEX.search(stripped):
            return ParsedOutputLine(
                raw_text=line,
                line_type="error",
                clean_text=stripped,
            )

        # Check Warning pattern
        if self.WARNING_REGEX.search(stripped):
            return ParsedOutputLine(
                raw_text=line,
                line_type="warning",
                clean_text=stripped,
            )

        # Check Prompt pattern
        if stripped == "-->" or line.startswith("-->"):
            return ParsedOutputLine(
                raw_text=line,
                line_type="prompt",
                clean_text=stripped,
            )

        return ParsedOutputLine(
            raw_text=line,
            line_type="stdout",
            clean_text=stripped,
        )
