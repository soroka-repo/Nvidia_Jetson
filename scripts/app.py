import paramiko
from flask import Flask, render_template, request
import os
import subprocess 

# --- Configuration ---
REMOTE_AI_NODES = [f"ai{i}" for i in range(1, 4)] 
LOCAL_HOST = "pi5"          
REMOTE_HOSTS = REMOTE_AI_NODES
ALL_TARGETS = REMOTE_AI_NODES + [LOCAL_HOST] 
USERNAME = os.environ.get('USER')
if not USERNAME:
    print("WARNING: USER environment variable not found. Falling back to 'soroka'.")
    USERNAME = "soroka"
PRIVATE_KEY_PATH = os.path.expanduser("~/.ssh/id_ed25519") 
# --- End Configuration ---

app = Flask(__name__)

# --- Service Management Constants ---
LLAMA_SERVICE_NAME = "llama-server"
# ------------------------------------

def execute_remote_command(host, command):
    # ... (execute_remote_command function remains the same) ...
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    stdout_output = ""
    stderr_output = ""
    
    try:
        print(f"Attempting to connect to {host}...")
        client.connect(
            hostname=host,
            username=USERNAME,
            key_filename=PRIVATE_KEY_PATH,
            timeout=20
        )
        
        stdin, stdout, stderr = client.exec_command(command)
        
        stdout_output = stdout.read().decode().strip()
        stderr_output = stderr.read().decode().strip()
        
    except paramiko.AuthenticationException:
        return None, "Authentication failed. Check username and key permissions."
    except paramiko.SSHException as e:
        return None, f"Could not establish SSH connection: {e}"
    except FileNotFoundError:
        return None, f"CRITICAL ERROR: Private key file not found at {PRIVATE_KEY_PATH}. Please verify the path."
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"
    finally:
        client.close()
        
    return stdout_output, stderr_output


def execute_local_command(command):
    # ... (execute_local_command function remains the same) ...
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr
    except Exception as e:
        return None, f"Local execution failed: {str(e)}"


def execute_command_on_host(host, command):
    """Determines whether to execute remotely or locally."""
    
    if host == LOCAL_HOST:
        return execute_local_command(command)

    elif host in REMOTE_HOSTS:
        # Since passwordless sudo is set up, we execute the command directly.
        return execute_remote_command(host, command)
    else:
        return None, f"Unknown host: {host}"


@app.route('/')
def index():
    """Renders the main dashboard interface."""
    return render_template('dashboard.html', hosts=ALL_TARGETS)


@app.route('/execute', methods=['POST'])
def execute_command():
    """Handles the command execution from the web form."""
    
    selected_hosts_str = request.form.getlist('target_host')
    command_input = request.form.get('command')

    if not command_input or not selected_hosts_str:
        return render_template('dashboard.html', output={"results": {}}, hosts=ALL_TARGETS)

    all_results = {}
    
    for host in selected_hosts_str:
        stdout, stderr = execute_command_on_host(host, command_input)
        all_results[host] = {"stdout": stdout, "stderr": stderr}
    
    return render_template('dashboard.html', 
                           output={"results": all_results},
                           hosts=ALL_TARGETS)

if __name__ == '__main__':
    print("===================================================")
    print("--- Starting Remote Command Dashboard ---")
    print(f"Detected Username: {USERNAME}")
    print(f"Targeting hosts: {', '.join(ALL_TARGETS)}")
    # *** FIX 1: Display the port ***
    print("===================================================")
    print("🎉 DASHBOARD IS RUNNING ON PORT 5000 🎉")
    print("===================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
