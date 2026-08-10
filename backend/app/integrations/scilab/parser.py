class ScilabOutputParser:
    @staticmethod
    def parse_output(stdout: str, stderr: str, max_size: int = 1048576) -> tuple[str, str, bool]:
        """
        Cleans Scilab prompt markers (e.g. '-->') and enforces max_size output limits.
        Returns (cleaned_stdout, cleaned_stderr, is_truncated).
        """
        is_truncated = False

        # Truncate stdout if needed
        if len(stdout.encode("utf-8")) > max_size:
            stdout = stdout.encode("utf-8")[:max_size].decode("utf-8", errors="ignore")
            stdout += "\n... [OUTPUT TRUNCATED DUE TO SIZE LIMIT]"
            is_truncated = True

        # Truncate stderr if needed
        if len(stderr.encode("utf-8")) > max_size:
            stderr = stderr.encode("utf-8")[:max_size].decode("utf-8", errors="ignore")
            stderr += "\n... [ERRORS TRUNCATED DUE TO SIZE LIMIT]"
            is_truncated = True

        # Filter out common prompt markers
        stdout_lines = [l for l in stdout.splitlines() if l.strip() != "-->"]
        stderr_lines = [l for l in stderr.splitlines() if l.strip() != "-->"]

        return "\n".join(stdout_lines), "\n".join(stderr_lines), is_truncated
