%define filelist kombu-4.1.0-filelist_python3

Name:           python3-kombu
Version:        4.1.0
Release:        1.%{?dist}
Summary:        python-kombu
Group:          Development/Languages
License:        BSD
URL:            https://kombu.readthedocs.io
Provides:       python3-kombu = %{version}-%{release}
Provides:       python3-kombu = %{version}-%{release}
Obsoletes:      python3-kombu < %{version}-%{release}
Obsoletes:      python3-kombu < %{version}-%{release}
BuildRequires:  python3-devel python3-rpm-macros python-srpm-macros

Requires: python3-kazoo
Requires: python3-PyYAML
Requires: python3-pycurl
Requires: python3-boto3
Requires: python3-sqlalchemy
Requires: python3-softlayer-messaging
Requires: python3-redis
Requires: python3-qpid-tools
Requires: python3-qpid-python
Requires: python3-pyro4
Requires: python3-msgpack-python
Requires: python3-pymongo
Requires: python3-librabbitmq
Requires: python3-python-consul
Requires: python3-amqp


%description


%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    rm -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/03/5e/1a47d1e543d4943d65330af4e4406049f443878818fb65bfdc651bb93a96/kombu-4.1.0.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
tar -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
mv %{_builddir}/kombu-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-kombu-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-kombu-%{version}-%{release}
[ "%{_builddir}/python2-kombu-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-kombu-%{version}-%{release}
[ "%{_builddir}/python3-kombu-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-kombu-%{version}-%{release}



%files -f %{filelist}

## end file