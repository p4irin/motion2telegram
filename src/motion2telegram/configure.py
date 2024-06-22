import os
import subprocess as sp

user = os.getenv('USER')
pwd = os.getenv('PWD')
module_dir = os.path.dirname(__file__)


def create_file_from_template(file: str, template: str) -> None:

    with open(template) as fh:

        template_content = fh.read()
        file_content = template_content.replace('{% user %}', user) # type: ignore
        file_content = file_content.replace('{% pwd %}', pwd) # type: ignore
        result = sp.run(
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
    sp.run(['cp', f'{module_dir}/template.motion.env', motion_env])
    sp.run(['chmod', 'u+rw-x', motion_env])
    sp.run(['chmod', 'g+r-wx', motion_env])
    sp.run(['chmod', 'o-rwx', motion_env])



def configure() -> None:

    motion_conf_template = f'{module_dir}/template.motion.conf'
    motion_conf = motion_conf_template.replace('template.', '')
    motion_service_template = f'{module_dir}/template.motion.service'
    motion_service = motion_service_template.replace('template.', '')
    mobile_phone_scan_service_template = f'{module_dir}/template.mobile_phone_scan.service'
    mobile_phone_scan_service = mobile_phone_scan_service_template.replace('template.', '')

    motion_is_enabled = sp.run(
        ['systemctl', 'is-enabled', 'motion.service'], capture_output=True
    ).stdout.decode().strip == 'enabled'

    if not motion_is_enabled:
        sp.run(['sudo', 'systemctl', 'enable', 'motion.service'])

    mobile_phone_scan_is_enabled = sp.run(
        ['systemctl', 'is-enabled', 'mobile_phone_scan.service'],
        capture_output=True
    ).stdout.decode().strip == 'enabled'

    if not mobile_phone_scan_is_enabled:
        sp.run(['sudo', 'systemctl', 'enable', 'mobile_phone_scan.service'])

    sp.run(['sudo', 'systemctl', 'stop', 'motion.service'])
    sp.run(['sudo', 'systemctl', 'stop', 'mobile_phone_scan.service'])

    create_file_from_template(motion_conf, motion_conf_template)
    create_file_from_template(motion_service, motion_service_template)
    create_file_from_template(mobile_phone_scan_service, mobile_phone_scan_service_template)

    command = [
        'cp', motion_conf, f'/etc/motion/{os.path.basename(motion_conf)}'
    ]
    sp.run(['sudo', '-S'] + command, check=True)
    command = [
        'cp', motion_service,
        f'/lib/systemd/system/{os.path.basename(motion_service)}'
    ]
    sp.run(['sudo', '-S'] + command, check=True)
    command = [
        'cp', mobile_phone_scan_service,
        f'/lib/systemd/system/{os.path.basename(mobile_phone_scan_service)}'
    ]
    sp.run(['sudo', '-S'] + command, check=True)
    sp.run(['sudo', 'systemctl', 'daemon-reload'])
    sp.run(['sudo', 'systemctl', 'start', 'motion.service'])
    sp.run(['sudo', 'systemctl', 'start', 'mobile_phone_scan.service'])

