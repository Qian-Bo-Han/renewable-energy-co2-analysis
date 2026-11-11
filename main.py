"""从项目根目录启动分析。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from renewable_pipeline.pipeline import main

if __name__ == "__main__":
    main()
