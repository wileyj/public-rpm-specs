%global with_alinux 1
%define filelist httpbin-0.6.2-filelist_python

Name:           python-httpbin
Version:        0.6.2
Release:        1.%{?dist}
Summary:        python-httpbin
Group:          Development/Languages
License:        MIT
URL:            https://github.com/kennethreitz/httpbin
Provides:       python-httpbin = %{version}-%{release}
Provides:       python-httpbin = %{version}-%{release}
Obsoletes:      python-httpbin < %{version}-%{release}
Obsoletes:      python-httpbin < %{version}-%{release}
BuildRequires:  python-devel python2-rpm-macros python-srpm-macros

Requires: python-six
Requires: python-raven[flask]
Requires: python-itsdangerous
Requires: python-flask-limiter
Requires: python-decorator
Requires: python-brotlipy
Requires: python-MarkupSafe
Requires: python-Flask-Common
Requires: python-Flask


%description


%if 0%{?with_alinux}
%package -n python27-httpbin
Summary:        python27-httpbin
Group:          Development/Languages
License:        MIT
URL:            https://github.com/kennethreitz/httpbin
Provides:       python27-httpbin = %{version}-%{release}
Provides:       python27-httpbin = %{version}-%{release}
Obsoletes:      python27-httpbin < %{version}-%{release}
Obsoletes:      python27-httpbin < %{version}-%{release}
BuildRequires:  python-devel python-rpm-macros python-srpm-macros

Requires: python27-six
Requires: python27-raven[flask]
Requires: python27-itsdangerous
Requires: python27-flask-limiter
Requires: python27-decorator
Requires: python27-brotlipy
Requires: python27-MarkupSafe
Requires: python27-Flask-Common
Requires: python27-Flask


%description -n python27-httpbin
** Amazon Linux Python

%endif

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    %{__rm} -rf %{_builddir}/%{name}-%{version}
fi
curl https://pypi.python.org/packages/63/01/5ed5d0d9a15f855fd82a99713a55ddaae70f8344327e4b2c676cba3494ff/httpbin-0.6.2.tar.gz  -o $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
 %{__tar} -xzvf $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz
%{__mv} %{_builddir}/httpbin-%{version} %{_builddir}/%{name}-%{version}
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
[ "%{_builddir}/python-httpbin-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python-python-httpbin-%{version}-%{release}
[ "%{_builddir}/python2-httpbin-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python2-python-httpbin-%{version}-%{release}
[ "%{_builddir}/python3-httpbin-%{version}-%{release}" != "/" ] && %__rm -rf %{_builddir}/python3-python-httpbin-%{version}-%{release}



%files -f %{filelist}

%if 0%{?with_alinux}
%files -n python27-httpbin -f %{filelist}
%endif

## end file