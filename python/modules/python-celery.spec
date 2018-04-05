%global with_alinux 1
%define filelist celery-4.1.0-filelist_python

Name:           python-celery
Version:        4.1.0
Release:        1.%{?dist}
Summary:        python-celery
Group:          Development/Languages
License:        BSD
URL:            http://celeryproject.org
Provides:       python-celery = %{version}-%{release}
Provides:       python-celery = %{version}-%{release}
Obsoletes:      python-celery < %{version}-%{release}
Obsoletes:      python-celery < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros

Requires: python-kazoo
Requires: python-PyYAML
Requires: python-tblib
Requires: python-pycurl
Requires: python-boto
Requires: python-sqlalchemy
Requires: python-ephem
Requires: python-softlayer-messaging
Requires: python-riak
Requires: python-redis
Requires: python-pyro4
Requires: python-python-memcached
Requires: python-msgpack-python
Requires: python-pylibmc
Requires: python-librabbitmq
Requires: python-gevent
Requires: python-eventlet
Requires: python-elasticsearch
Requires: python-boto3
Requires: python-Django
Requires: python-python-consul
Requires: python-cassandra-driver
Requires: python-pyOpenSSL
Requires: python-pytz
Requires: python-kombu
Requires: python-billiard


%description


%if 0%{?with_alinux}
%package -n python27-celery
Summary:        python27-celery
Group:          Development/Languages
License:        BSD
URL:            http://celeryproject.org
Provides:       python27-celery = %{version}-%{release}
Provides:       python27-celery = %{version}-%{release}
Obsoletes:      python27-celery < %{version}-%{release}
Obsoletes:      python27-celery < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros

Requires: python27-kazoo
Requires: python27-PyYAML
Requires: python27-tblib
Requires: python27-pycurl
Requires: python27-boto
Requires: python27-sqlalchemy
Requires: python27-ephem
Requires: python27-softlayer-messaging
Requires: python27-riak
Requires: python27-redis
Requires: python27-pyro4
Requires: python27-python-memcached
Requires: python27-msgpack-python
Requires: python27-pylibmc
Requires: python27-librabbitmq
Requires: python27-gevent
Requires: python27-eventlet
Requires: python27-elasticsearch
Requires: python27-boto3
Requires: python27-Django
Requires: python27-python-consul
Requires: python27-cassandra-driver
Requires: python27-pyOpenSSL
Requires: python27-pytz
Requires: python27-kombu
Requires: python27-billiard


%description -n python27-celery
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/07/65/88a2a45fc80f487872c93121a701a53bbbc3d3d832016876fac84fc8d46a/celery-4.1.0.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/celery-%{version} %{_builddir}/%{name}-%{version}
%{__chmod} -R u+w %{_builddir}/%{name}-%{version}
cd $RPM_BUILD_DIR/%{name}-%{version}

%__rm -rf %{py2dir}
%__cp -a . %{py2dir}


%build
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py2dir}
%{__python27} setup.py build
popd


%install
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py2dir}
%{__python27} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%{__perl} -MFile::Find -le '
    find ({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    for my $x (sort @dirs, @files) {
        push @ret, $x unless indirs($x);
    }
    print join "\n", sort @ret;
    sub wanted {
        return if /auto$/;
        local $_ = $File::Find::name;
        my $f = $_; s|^\Q%{buildroot}\E||;
        return unless length;
        return $files[@files] = $_ if -f $f;
        $d = $_;
        /\Q$d\E/ && return for reverse sort @INC;
        $d =~ /\Q$_\E/ && return
            for qw|/etc %_prefix/man %_prefix/bin %_prefix/share|;
        $dirs[@dirs] = $_;
      }

    sub indirs {
        my $x = shift;
        $x =~ /^\Q$_\E\// && $x ne $_ && return 1 for @dirs;
    }
' > $RPM_BUILD_DIR//%{filelist}
%__sed -i -e 's/.*/\"&\"/g' $RPM_BUILD_DIR/%{filelist}
exit 0


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/python-celery-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-celery-%{version}-%{release}
[ "%{_builddir}/python2-celery-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-celery-%{version}-%{release}
[ "%{_builddir}/python3-celery-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-celery-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-celery -f %{filelist}
%endif

## end file