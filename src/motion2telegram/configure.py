import os
import subprocess

user = os.getenv('USER')
pwd = os.getenv('PWD')
module_path = os.path.dirname(os.path.abspath(__file__))


def create_file_from_template(file_path: str, template_path: str) -> None:
    with open(template_path) as fh:
        template_content = fh.read()
        file_content = template_content.replace('{% user %}', user) # type: ignore
        file_content = file_content.replace('{% pwd %}', pwd) # type: ignore
        output = subprocess.run(['which', 'motion2telegram'], capture_output=True)
        file_content = file_content.replace('{% motion2telegram %}', output.stdout.decode().strip())

    with open(file_path, 'w') as fh:
        fh.write(file_content)


def init() -> None:
    """Create a 'motion.env' file in the users' current working directory
    
    and set permissions on the file.
    Allow the user read and write access.
    Allow the group read access.
    Disallow access for anyone else.
    """

    motion_env_path = f'{pwd}/motion.env'
    subprocess.run(['cp', f'{module_path}/template.motion.env', motion_env_path])
    subprocess.run(['chmod', 'u+rw-x', motion_env_path])
    subprocess.run(['chmod', 'g+r-wx', motion_env_path])
    subprocess.run(['chmod', 'o-rwx', motion_env_path])



def configure() -> None:
    motion_conf_template_path = f'{module_path}/template.motion.conf'
    motion_conf_path = motion_conf_template_path.replace('template.', '')
    motion_service_template_path = f'{module_path}/template.motion.service'
    motion_service_path = motion_service_template_path.replace('template.', '')

    subprocess.run(['sudo', 'systemctl', 'stop', 'motion.service'])

    create_file_from_template(motion_conf_path, motion_conf_template_path)
    create_file_from_template(motion_service_path, motion_service_template_path)

    command = [
        'cp', motion_conf_path, f'/etc/motion/{os.path.basename(motion_conf_path)}'
    ]
    subprocess.run(['sudo', '-S'] + command, check=True)
    command = [
        'cp', motion_service_path,
        f'/lib/systemd/system/{os.path.basename(motion_service_path)}'
    ]
    subprocess.run(['sudo', '-S'] + command, check=True)
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'])
    subprocess.run(['sudo', 'systemctl', 'start', 'motion.service'])
