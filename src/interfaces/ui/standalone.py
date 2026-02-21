import threading
import time
import webview
import sys
import os
import logging
from src.interfaces.ui.gradio_app import demo

# Setup logging to a file in the project root
logging.basicConfig(
    filename='logs/app_runtime.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def launch_gradio():
    """Starts the Gradio server and returns the local URL."""
    try:
        logging.info("Attempting to launch Gradio server...")
        # launch() returns the FastAPI app, local URL, and share URL
        result = demo.launch(
            prevent_thread_lock=True, 
            show_error=True,
            quiet=False,
            inbrowser=False # Don't open the browser automatically
        )
        # Check if result is a tuple (app, local_url, share_url) or just local_url
        if isinstance(result, tuple):
            _, local_url, _ = result
        else:
            local_url = result
            
        logging.info(f"Gradio server started at: {local_url}")
        return local_url
    except Exception as e:
        logging.error(f"Failed to launch Gradio server: {str(e)}", exc_info=True)
        return None

if __name__ == "__main__":
    try:
        if not os.path.exists("logs"):
            os.makedirs("logs")

        logging.info("--- Application Starting ---")
        
        # 1. Start Gradio
        url = launch_gradio()
        
        if not url:
            logging.error("No URL returned from Gradio. Exiting.")
            sys.exit(1)

        # 2. Give it a tiny bit of time to settle
        time.sleep(1)

        # 3. Create a native desktop window
        logging.info("Creating native window...")
        webview.create_window(
            title="Bible Quiz Automation",
            url=url,
            width=1200,
            height=800,
            min_size=(800, 600)
        )

        # 4. Start the window
        logging.info("Starting WebView main loop...")
        webview.start()
        logging.info("WebView main loop exited.")

    except Exception as e:
        logging.critical(f"Standalone wrapper encountered a fatal error: {str(e)}", exc_info=True)
        # On Windows, we want to make sure the user sees this before the console closes
        print(f"\nFATAL ERROR: {str(e)}")
        print("Please check logs/app_runtime.log for details.")
        input("Press Enter to close...")
        sys.exit(1)
