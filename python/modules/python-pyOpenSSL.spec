%global with_alinux 1
%define filelist pyOpenSSL-17.4.0-filelist_python

Name:           python-pyOpenSSL
Version:        17.4.0
Release:        1.%{?dist}
Summary:        python-pyOpenSSL
Group:          Development/Languages
License:        Apache License, Version 2.0
URL:            https://pyopenssl.org/
Provides:       python-pyOpenSSL = %{version}-%{release}
Provides:       python-pyopenssl = %{version}-%{release}
Obsoletes:      python-pyOpenSSL < %{version}-%{release}
Obsoletes:      python-pyopenssl < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros

Requires: python-pytest
Requires: python-pretend
Requires: python-flaky
Requires: python-sphinx
Requires: python-six
Requires: python-cryptography


%description


%if 0%{?with_alinux}
%package -n python27-pyOpenSSL
Summary:        python27-pyOpenSSL
Group:          Development/Languages
License:        Apache License, Version 2.0
URL:            https://pyopenssl.org/
Provides:       python27-pyOpenSSL = %{version}-%{release}
Provides:       python27-pyopenssl = %{version}-%{release}
Obsoletes:      python27-pyOpenSSL < %{version}-%{release}
Obsoletes:      python27-pyopenssl < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros

Requires: python27-pytest
Requires: python27-pretend
Requires: python27-flaky
Requires: python27-sphinx
Requires: python27-six
Requires: python27-cryptography


%description -n python27-pyOpenSSL
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/41/63/8759b18f0a240e91a24029e7da7c4a95ab75bca9028b02635ae0a9723c23/pyOpenSSL-17.4.0.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/pyOpenSSL-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-pyOpenSSL-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-pyOpenSSL-%{version}-%{release}
[ "%{_builddir}/python2-pyOpenSSL-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-pyOpenSSL-%{version}-%{release}
[ "%{_builddir}/python3-pyOpenSSL-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-pyOpenSSL-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-pyOpenSSL -f %{filelist}
%endif

## end file
