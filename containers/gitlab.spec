%define repo https://gitlab.com/gitlab-org/gitlab-ce
%define gitversion %(echo `curl -s %{repo}/releases | grep 'span class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">vr'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1`)
%define rel_version 1

%define gitlab_uid 65434
%define gitlab_gid 65434
%define _use_internal_dependency_generator 0

%define     homedir       %{_localstatedir}/lib/gitlab

Name:          gitlab
Version:       %{gitversion}
Release:       %{rel_version}.%{revision}.%{dist}
Summary:       A Web interface to create projects and repositories, manage access and do code reviews
Group:         Applications/Web
Vendor:        openmamba
Distribution:  openmamba
Packager:      Silvan Calarco <silvan.calarco@...>
URL:           https://www.gitlab.com/gitlab-ce/
## GITSOURCE https://gitlab.com/gitlab-org/gitlab-ce.git v6.9.0
Source:        https://gitlab.com/gitlab-org/gitlab-ce.git/v%{version}/gitlab-ce-%{version}.tar.bz2
License:       MIT
Source1:       gitlab.target
Source2:       gitlab-sidekiq.service
Source3:       gitlab-unicorn.service
Source4:       gitlab.logrotate
Source5:       gitlab.tmpfiles.d
Source6:       gitlab-apache-conf
## AUTOBUILDREQ-BEGIN
## AUTOBUILDREQ-END
BuildRequires: ruby-bundler
Requires:      ruby-bundler
Requires:      redis
Requires:      mysql-server
Requires:      apache
Requires:      git
Requires(pre): gitlab-shell
BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
GitLab Community Edition (CE) is open source software to collaborate on code. 
Create projects and repositories, manage access and do code reviews. 
GitLab CE is on-premises software that you can install and use on your server(s).

%prep
%setup -q -n %{name}-ce-%{version} -D -T
#:<< _EOF

# Patching config files:
sed -e "s|# user: git|user: gitlab|" \
	-e "s|/home/git/repositories|%{homedir}/repositories|" \
	-e "s|/home/git/gitlab-satellites|%{homedir}/satellites|" \
	-e "s|/home/git/gitlab-shell|/usr/share/gitlab-shell|" \
	config/gitlab.yml.example > config/gitlab.yml
sed -e "s|/home/git/gitlab/tmp/.*/|/run/gitlab/|g" \
	-e "s|/home/git/gitlab|%{homedir}|g" \
	-e "s|/usr/share/gitlab/log|%{homedir}/log|g" \
	-e "s|timeout 30|timeout 300|" \
	config/unicorn.rb.example > config/unicorn.rb
sed -e "s|username: git|username: gitlab|" \
	config/database.yml.mysql > config/database.yml
		
%build
:<< _EOF
# Note: SSL error temporary fixed with 'sudo gem update --system' which updates
# /usr/bin/gem

bundle install %{_smp_mflags} \
   --no-cache --no-prune --deployment --without development test aws

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
install -d \
    %{buildroot}%{homedir}/www \
    %{buildroot}%{homedir}/public/uploads \
	%{buildroot}%{_sysconfdir}/gitlab \
    %{buildroot}%{_docdir}/gitlab \
    %{buildroot}%{homedir}/satellites

cp -a . %{buildroot}%{homedir}/

# Creating links
ln -fs /run/gitlab %{buildroot}%{homedir}/pids
ln -fs /run/gitlab %{buildroot}%{homedir}/sockets
ln -fs %{_localstatedir}/log/gitlab %{buildroot}%{homedir}/log
install -d -m0755 %{_localstatedir}/log/gitlab

# Install config files
for f in gitlab.yml unicorn.rb database.yml; do
	install -m0644 config/$f %{buildroot}%{_sysconfdir}/gitlab/$f
	[[ -f "%{buildroot}%{homedir}/config/$f" ]] && rm %{buildroot}%{homedir}/config/$f
	ln -fs %{_sysconfdir}/gitlab/$f %{buildroot}%{homedir}/config/
done

# Install systemd service files
install -D -m0644 %{S:1} %{buildroot}/lib/systemd/system/gitlab.target
install -D -m0644 %{S:2} %{buildroot}/lib/systemd/system/gitlab-sidekiq.service
install -D -m0644 %{S:3} %{buildroot}/lib/systemd/system/gitlab-unicorn.service
install -D -m0644 %{S:4} %{buildroot}%{_sysconfdir}/logrotate.d/gitlab.logrotate
install -D -m0644 %{S:5} %{buildroot}%{_prefix}/lib/tmpfiles.d/gitlab.conf
install -D -m0644 %{S:6} %{buildroot}%{_sysconfdir}/httpd/httpd.d/gitlab.conf

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%pre
if [ $1 -ge 1 ]; then
   /usr/sbin/groupadd gitlab -g %{gitlab_gid} 2>/dev/null
   /usr/sbin/useradd -u %{gitlab_uid} -c 'Gitlab user' -d %{homedir} -g gitlab \
      -s /bin/bash gitlab 2>/dev/null
fi
:

%post
if [ $1 -ge 1 ]; then
  systemctl -q daemon-reload
  systemd-tmpfiles --create %{_prefix}/lib/tmpfiles.d/gitlab.conf
  [ -e %{_localstatedir}/lock/subsys/httpd ] && service httpd reload || :
fi
if [ $1 -eq 1 ]; then
   systemctl -q enable gitlab-unicorn
   systemctl -q enable gitlab-sidekiq
   systemctl -q enable gitlab.target
   systemctl -q start gitlab-unicorn
   systemctl -q start gitlab-sidekiq
   systemctl -q start gitlab.target
   sudo -u gitlab -H git config --global user.name "GitLab"
   sudo -u gitlab -H git config --global user.email "gitlab@localhost"
   sudo -u gitlab -H git config --global core.autocrlf input
   echo "Create and configure database in /etc/gitlab/database.yml"
   echo "Then run 'sudo -u gitlab bundle exec rake gitlab:setup RAILS_ENV=production'"
   echo
else
   systemctl -q try-restart gitlab-unicorn
   systemctl -q try-start gitlab-sidekiq
fi
:

%postun
if [ $1 -eq 0 ]; then
   /usr/sbin/userdel gitlab 2>/dev/null
   /usr/sbin/groupdel gitlab 2>/dev/null
fi
:

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/gitlab
%config(noreplace) %{_sysconfdir}/gitlab/database.yml
%config(noreplace) %{_sysconfdir}/gitlab/gitlab.yml
%config(noreplace) %{_sysconfdir}/gitlab/unicorn.rb
%config(noreplace) %{_sysconfdir}/httpd/httpd.d/%{name}.conf
%{_sysconfdir}/logrotate.d/gitlab.logrotate
/lib/systemd/system/gitlab-sidekiq.service
/lib/systemd/system/gitlab-unicorn.service
/lib/systemd/system/gitlab.target
%{_prefix}/lib/tmpfiles.d/gitlab.conf
%dir %attr(0755,gitlab,gitlab) %{homedir}
%attr(-,gitlab,gitlab) %{homedir}/*
%dir %attr(0755,gitlab,gitlab) %{homedir}/satellites
%attr(-,gitlab,gitlab) %{homedir}/.*
%doc LICENSE

