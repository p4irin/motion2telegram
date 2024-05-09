import os
import subprocess

user = os.getenv('USER')
root_path = os.path.dirname(os.path.abspath(__file__))
motion_conf_template_path = f'{root_path}/template.motion.conf'
motion_conf_path = motion_conf_template_path.replace('template.', '')
motion_service_template_path = f'{root_path}/template.motion.service'
motion_service_path = motion_service_template_path.replace('template.', '')


def create_file_from_template(file_path: str, template_path: str) -> None:
    with open(template_path) as fh:
        template_content = fh.read()
        file_content = template_content.replace('{% user %}', user)

    with open(file_path, 'w') as fh:
        fh.write(file_content)


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
