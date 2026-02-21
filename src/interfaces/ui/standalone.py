import threading
import time
import webview
from src.interfaces.ui.gradio_app import demo

def launch_gradio():
    """Starts the Gradio server in a background thread."""
    # prevent_thread_lock=True allows the script to continue to the webview part
    demo.launch(prevent_thread_lock=True, show_error=True)

if __name__ == "__main__":
    # 1. Start Gradio in the background
    t = threading.Thread(target=launch_gradio)
    t.daemon = True
    t.start()

    # 2. Wait a moment for the server to spin up
    time.sleep(2)

    # 3. Create a native desktop window
    # By default, Gradio runs on http://127.0.0.1:7860
    window = webview.create_window(
        title="Bible Quiz Automation",
        url="http://127.0.0.1:7860",
        width=1200,
        height=800,
        min_size=(800, 600),
        confirm_close=False
    )

    # 4. Start the window (this is a blocking call)
    # When the window is closed, the script will exit
    webview.start()
