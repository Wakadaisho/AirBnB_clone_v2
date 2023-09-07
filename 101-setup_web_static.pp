# Install nginx, setup release directories and files

package {'nginx':
  ensure => present
}

file {['/data',
'/data/web_static',
'/data/web_static/releases',
'/data/web_static/releases/test']:
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true
}

file {'/data/web_static/releases/test/index.html':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  content => 'Hello NGINX'
  notify  => 'sym_link'
}

file_line {'hbnb_static':
  path  => '/etc/nginx/sites-available/default',
  after => '^server',
  line  => '	location /hbnb_static {
			alias '/data/web_static/current';
	}'
}

exec {'sym_link':
  command => 'ln -sf /data/web_static/releases/test /data/web_static/current',
  owner   => 'ubuntu',
  group   => 'ubuntu'
}
service {'nginx':
  ensure     => running,
  enable     => true,
  hasrestart => true
}

