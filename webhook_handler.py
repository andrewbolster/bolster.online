from flask import Flask, request
import subprocess
import markdown2

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Pull the repository
        subprocess.run(['git', 'pull'])

        # Convert index.md to index.html
        with open('index.md', 'r') as md_file:
            md_content = md_file.read()
            html_content = markdown2.markdown(md_content)
            with open('index.html', 'w') as html_file:
                html_file.write(html_content)

        # Push index.html to ~/www_root/index.html
        subprocess.run(['cp', 'index.html', '~/www_root/index.html'])

        # Restart nginx service
        subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])

        return 'Webhook received and processed', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
