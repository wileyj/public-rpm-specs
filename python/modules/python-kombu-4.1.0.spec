%global with_alinux 1
%define filelist kombu-4.1.0-filelist_python

Name:           python-kombu
Version:        4.1.0
Release:        1.%{?dist}
Summary:        python-kombu
Group:          Development/Languages
License:        BSD
URL:            https://kombu.readthedocs.io
Provides:       python-kombu = %{version}-%{release}
Provides:       python-kombu = %{version}-%{release}
Obsoletes:      python-kombu < %{version}-%{release}
Obsoletes:      python-kombu < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros

Requires: python-kazoo
Requires: python-PyYAML
Requires: python-pycurl
Requires: python-boto3
Requires: python-sqlalchemy
Requires: python-softlayer-messaging
Requires: python-redis
Requires: python-qpid-tools
Requires: python-qpid-python
Requires: python-pyro4
Requires: python-msgpack-python
Requires: python-pymongo
Requires: python-librabbitmq
Requires: python-python-consul
Requires: python-amqp


%description


%if 0%{?with_alinux}
%package -n python27-kombu
Summary:        python27-kombu
Group:          Development/Languages
License:        BSD
URL:            https://kombu.readthedocs.io
Provides:       python27-kombu = %{version}-%{release}
Provides:       python27-kombu = %{version}-%{release}
Obsoletes:      python27-kombu < %{version}-%{release}
Obsoletes:      python27-kombu < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros

Requires: python27-kazoo
Requires: python27-PyYAML
Requires: python27-pycurl
Requires: python27-boto3
Requires: python27-sqlalchemy
Requires: python27-softlayer-messaging
Requires: python27-redis
Requires: python27-qpid-tools
Requires: python27-qpid-python
Requires: python27-pyro4
Requires: python27-msgpack-python
Requires: python27-pymongo
Requires: python27-librabbitmq
Requires: python27-python-consul
Requires: python27-amqp


%description -n python27-kombu
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/03/5e/1a47d1e543d4943d65330af4e4406049f443878818fb65bfdc651bb93a96/kombu-4.1.0.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/kombu-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-kombu-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-kombu-%{version}-%{release}
[ "%{_builddir}/python2-kombu-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-kombu-%{version}-%{release}
[ "%{_builddir}/python3-kombu-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-kombu-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-kombu -f %{filelist}
%endif

## end file