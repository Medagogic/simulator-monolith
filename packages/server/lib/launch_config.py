import argparse

class LaunchConfig:
    @staticmethod
    def noFrontend() -> bool:
        parser = argparse.ArgumentParser(description="Check launch options for FastAPI server.")
        parser.add_argument('--no-frontend', action='store_true', help='Launch without frontend')
        args = parser.parse_args()
        
        return args.no_frontend
