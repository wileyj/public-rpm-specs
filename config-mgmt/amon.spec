# https://docs.amon.cx/onpremise/
# useradd --system --user-group --key USERGROUPS_ENAB=yes -M amon --shell /bin/false -d /etc/opt/amon


%define git_repo https://github.com/amonapp/amon
%define git_version %(echo `curl -s  %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global git_revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define git_summary        %(echo `curl -s %{repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define rel_version 1
%define app_prefix /opt/%{name}-%{version}
%define app_logdir /var/log/%{name}
%define app_configdir %{app_prefix}%{sysconfdir}
%define app_user %{name]
%define app_group %{name]

Name:           amon
Version:        %{git_version}
Release:        %{rel_version}.%{git_revision}.%{dist}
Summary:        %{git_sumamry}
Group:          System Environment/Base
License:       	AGPL-3.0 
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:            %{git_url}
BuildRequires: 	python3 git
Requires:	python3

Requires: python3-beautifulsoup4 >= 4.5.1
Requires: python3-Django >= 1.9.12
Requires: python3-django-annoying >= 0.10.3
Requires: python3-django-kronos >= 1.0
Requires: python3-django-timezone-field >= 2.0
Requires: python3-djangorestframework >= 3.5.3
Requires: python3-pyaml >= 16.12.2
Requires: python3-pymongo >= 3.4.0
Requires: python3-python-dateutil >= 2.6.0
Requires: python3-pytz >= 2016.10
Requires: python3-requests >= 2.12.4
Requires: python3-pycrypto >= 2.6.1
Requires: python3-gunicorn >= 19.6.0
Requires: python3-gevent >= 1.2.0
Requires: python3-wheel >= 0.29.0
Requires: python3-xmltodict >= 0.10.2
Requires: python3-boto >= 2.45.0
Requires: python3-apache-libcloud >= 1.5.0
Requires: python3-django-storages >= 1.5.1
Requires: python3-virtuvalenv 

#BuildRequires: python3-yanc >= 0.3.3
#BuildRequires: python3-nose >= 1.3.7
#BuildRequires: python3-nose-exclude >= 0.5.0
#BuildRequires: python3-nose-timer >= 0.6.0
#BuildRequires: python3-Faker >= 0.7.7
#BuildRequires: python3-django-nose >= 1.4.4

%description
%{git_summary}

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}


%install
cd %{name}-%{version}
rm -rf %{buildroot}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%defattr(-,root,root,-)

%changelog
