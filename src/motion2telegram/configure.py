import os
import subprocess

user = os.getenv('USER')
pwd = os.getenv('PWD')
module_dir = os.path.dirname(__file__)


def create_file_from_template(file: str, template: str) -> None:

    with open(template) as fh:

        template_content = fh.read()
        file_content = template_content.replace('{% user %}', user) # type: ignore
        file_content = file_content.replace('{% pwd %}', pwd) # type: ignore
        result = subprocess.run(
            ['which', 'motion2telegram'],
            capture_output=True
        )
        file_content = file_content.replace(
            '{% motion2telegram %}', result.stdout.decode().strip()
        )

    with open(file, 'w') as fh:

        fh.write(file_content)


def init() -> None:
    """Create a 'motion.env' file in the users' current working directory
    
    and set permissions on the file.
    Allow the user read and write access.
    Allow the group read access.
    Disallow access for anyone else.
    """

    motion_env = f'{pwd}/motion.env'
    subprocess.run(['cp', f'{module_dir}/template.motion.env', motion_env])
    subprocess.run(['chmod', 'u+rw-x', motion_env])
    subprocess.run(['chmod', 'g+r-wx', motion_env])
    subprocess.run(['chmod', 'o-rwx', motion_env])



def configure() -> None:

    motion_conf_template = f'{module_dir}/template.motion.conf'
    motion_conf = motion_conf_template.replace('template.', '')
    motion_service_template = f'{module_dir}/template.motion.service'
    motion_service = motion_service_template.replace('template.', '')
    mobile_phone_scan_service_template = f'{module_dir}/template.mobile_phone_scan.service'
    mobile_phone_scan_service = mobile_phone_scan_service_template.replace('template.', '')

    subprocess.run(['sudo', 'systemctl', 'stop', 'motion.service'])
    subprocess.run(['sudo', 'systemctl', 'stop', 'mobile_phone_scan.service'])

    create_file_from_template(motion_conf, motion_conf_template)
    create_file_from_template(motion_service, motion_service_template)
    create_file_from_template(mobile_phone_scan_service, mobile_phone_scan_service_template)

    command = [
        'cp', motion_conf, f'/etc/motion/{os.path.basename(motion_conf)}'
    ]
    subprocess.run(['sudo', '-S'] + command, check=True)
    command = [
        'cp', motion_service,
        f'/lib/systemd/system/{os.path.basename(motion_service)}'
    ]
    subprocess.run(['sudo', '-S'] + command, check=True)
    command = [
        'cp', mobile_phone_scan_service,
        f'/lib/systemd/system/{os.path.basename(mobile_phone_scan_service)}'
    ]
    subprocess.run(['sudo', '-S'] + command, check=True)
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'])
    subprocess.run(['sudo', 'systemctl', 'start', 'motion.service'])
    subprocess.run(['sudo', 'systemctl', 'start', 'mobile_phone_scan.service'])

