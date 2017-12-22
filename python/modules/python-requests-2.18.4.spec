%global with_alinux 1
%define filelist requests-2.18.4-filelist_python

Name:           python-requests
Version:        2.18.4
Release:        1.%{?dist}
Summary:        python-requests
Group:          Development/Languages
License:        Apache 2.0
URL:            http://python-requests.org
Provides:       python-requests = %{version}-%{release}
Provides:       python-requests = %{version}-%{release}
Obsoletes:      python-requests < %{version}-%{release}
Obsoletes:      python-requests < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros

Requires: python-PySocks
Requires: python-pyOpenSSL
Requires: python-idna
Requires: python-cryptography
Requires: python-urllib3
Requires: python-idna
Requires: python-chardet
Requires: python-certifi


%description


%if 0%{?with_alinux}
%package -n python27-requests
Summary:        python27-requests
Group:          Development/Languages
License:        Apache 2.0
URL:            http://python-requests.org
Provides:       python27-requests = %{version}-%{release}
Provides:       python27-requests = %{version}-%{release}
Obsoletes:      python27-requests < %{version}-%{release}
Obsoletes:      python27-requests < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros

Requires: python27-PySocks
Requires: python27-pyOpenSSL
Requires: python27-idna
Requires: python27-cryptography
Requires: python27-urllib3
Requires: python27-idna
Requires: python27-chardet
Requires: python27-certifi


%description -n python27-requests
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/b0/e1/eab4fc3752e3d240468a8c0b284607899d2fbfb236a56b7377a329aa8d09/requests-2.18.4.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/requests-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-requests-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-requests-%{version}-%{release}
[ "%{_builddir}/python2-requests-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-requests-%{version}-%{release}
[ "%{_builddir}/python3-requests-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-requests-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-requests -f %{filelist}
%endif

## end file
