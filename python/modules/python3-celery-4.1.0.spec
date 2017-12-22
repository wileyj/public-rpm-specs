%define filelist celery-4.1.0-filelist_python3

Name:           python3-celery
Version:        4.1.0
Release:        1.%{?dist}
Summary:        python-celery
Group:          Development/Languages
License:        BSD
URL:            http://celeryproject.org
Provides:       python3-celery = %{version}-%{release}
Provides:       python3-celery = %{version}-%{release}
Obsoletes:      python3-celery < %{version}-%{release}
Obsoletes:      python3-celery < %{version}-%{release}
BuildRequires:  python3-devel python3-rpm-macros python-srpm-macros

Requires: python3-kazoo
Requires: python3-PyYAML
Requires: python3-tblib
Requires: python3-pycurl
Requires: python3-boto
Requires: python3-sqlalchemy
Requires: python3-ephem
Requires: python3-softlayer-messaging
Requires: python3-riak
Requires: python3-redis
Requires: python3-pyro4
Requires: python3-python-memcached
Requires: python3-msgpack-python
Requires: python3-pylibmc
Requires: python3-librabbitmq
Requires: python3-gevent
Requires: python3-eventlet
Requires: python3-elasticsearch
Requires: python3-boto3
Requires: python3-Django
Requires: python3-python-consul
Requires: python3-cassandra-driver
Requires: python3-pyOpenSSL
Requires: python3-pytz
Requires: python3-kombu
Requires: python3-billiard


%description


%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    rm -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/07/65/88a2a45fc80f487872c93121a701a53bbbc3d3d832016876fac84fc8d46a/celery-4.1.0.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
tar -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
mv %{_builddir}/celery-%{version} %{_builddir}/%{name}-%{version}
chmod -R u+w %{_builddir}/%{name}-%{version}
cd $RPM_BUILD_DIR/%{name}-%{version}

rm -rf %{py3dir}
cp -a . %{py3dir}


%build
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py3dir}
%{__python3} setup.py build
popd


%install
cd $RPM_BUILD_DIR/%{name}-%{version}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
find %{buildroot}%{_prefix} -type d -depth -exec rmdir {} \; 2>/dev/null
popd
%{__perl} -MFile::Find -le '
    find({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    #print "%doc  src Changes examples README";
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
%{__sed} -i -e 's/.*/\"&\"/g' $RPM_BUILD_DIR//%{filelist}
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

## end file