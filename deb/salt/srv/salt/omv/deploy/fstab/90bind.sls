{% set mountpoints = salt['omv.get_config_by_filter'](
  'conf.system.filesystem.mountpoint',
  '{"operator": "and", "arg0": {"operator": "equals", "arg0": "hidden", "arg1": "0"}, "arg1": {"operator": "stringContains", "arg0": "opts", "arg1": "bind"}}') %}

{% for mountpoint in mountpoints %}
create_bind_mountpoint_{{ mountpoint.uuid }}:
  file.accumulated:
    - filename: "/etc/fstab"
    - text: "{{ mountpoint.fsname | replace('\\ ','\\040') }}\t\t{{ mountpoint.dir }}\t{{ mountpoint.type }}\t{{ mountpoint.opts }}\t{{ mountpoint.freq }} {{ mountpoint.passno }}"
    - require_in:
      - file: append_fstab_entries
{% endfor %}
