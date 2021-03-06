%global with_alinux 1
%define filelist paramiko-2.4.0-filelist_python

Name:           python-paramiko
Version:        2.4.0
Release:        1.%{?dist}
Summary:        python-paramiko
Group:          Development/Languages
License:        LGPL
URL:            https://github.com/paramiko/paramiko/
Provides:       python-paramiko = %{version}-%{release}
Provides:       python-paramiko = %{version}-%{release}
Obsoletes:      python-paramiko < %{version}-%{release}
Obsoletes:      python-paramiko < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros

Requires: python-pyasn1
Requires: python-pynacl
Requires: python-cryptography
Requires: python-bcrypt


%description


%if 0%{?with_alinux}
%package -n python27-paramiko
Summary:        python27-paramiko
Group:          Development/Languages
License:        LGPL
URL:            https://github.com/paramiko/paramiko/
Provides:       python27-paramiko = %{version}-%{release}
Provides:       python27-paramiko = %{version}-%{release}
Obsoletes:      python27-paramiko < %{version}-%{release}
Obsoletes:      python27-paramiko < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros

Requires: python27-pyasn1
Requires: python27-pynacl
Requires: python27-cryptography
Requires: python27-bcrypt


%description -n python27-paramiko
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/c8/de/791773d6a4b23327c7475ae3d7ada0d07fa147bf77fb6f561a4a7d8afd11/paramiko-2.4.0.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/paramiko-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-paramiko-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-paramiko-%{version}-%{release}
[ "%{_builddir}/python2-paramiko-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-paramiko-%{version}-%{release}
[ "%{_builddir}/python3-paramiko-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-paramiko-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-paramiko -f %{filelist}
%endif

## end file