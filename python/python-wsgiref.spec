%define pkgname wsgiref
%define pexec python27
%define pip_version %(echo `curl -s https://pypi.python.org/pypi/%{pkgname} | grep "<title>" | awk '{print $2}'`)
%define filelist %{pkgname}-%{version}-filelist

Name:           %{pexec}-%{pkgname}
Version:        %{pip_version}
Release:        1.%{dist}
Summary:        standalone release of the wsgiref library
Group:          Development/Languages
License:        BSD
Packager:       %{packager}
Vendor:         %{vendor}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27, python27-devel, python27-setuptools
BuildRequires: git python-srpm-macros
Requires:       python27

%include /usr/lib/rpm/macros.d/macros.python
%description
This is a standalone release of the wsgiref library, that provides validation support for WSGI 1.0.1 (PEP 3333) for Python versions < 3.2, and includes the new wsgiref.util.test() utility function.

%prep
if [ -d %{_builddir}/%{name}-%{version} ];then
    rm -rf %{_builddir}/%{name}-%{version}
fi
curl -o $RPM_SOURCE_DIR/%{name}.zip `curl -s https://pypi.python.org/pypi/%{pkgname} | grep ".zip" | cut -d '"' -f2 | cut -f1 -d "#" | head -1`
unzip $RPM_SOURCE_DIR/%{name}.zip
mv %{_builddir}/%{pkgname}-%{version} %{_builddir}/%{name}-%{version}
chmod -R u+w %{_builddir}/%{name}-%{version}

%build
cd $RPM_BUILD_DIR/%{name}-%{version}
%{__python} setup.py build

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

# no empty directories
find %{buildroot}%{_prefix}             \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null

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
    ' > %filelist

[ -z %filelist ] && {
    echo "ERROR: empty %files listing"
    exit -1
    }

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}

%files -f %{name}-%{version}/%filelist
%defattr(-,root,root)

%changelog
