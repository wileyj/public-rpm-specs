%define repo https://github.com/pypa/setuptools
%define pkgname setuptools
%define pexec python27
%define pip_version %(echo `curl -s https://pypi.python.org/pypi/%{pkgname} | grep "<title>" | awk '{print $2}'`)
%define filelist %{pkgname}-%{version}-filelist

Name:           %{pexec}-%{pkgname}
Version:        %{pip_version}
Release:        1.%{dist}
Summary:        Easily download, build, install, upgrade, and uninstall Python packages
Group:          Development/Languages
License:        BSD
Packager:       %{packager}
Vendor:         %{vendor}
URL:            http://pypi.python.org/pypi/redis
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python27, python27-devel, python27-setuptools
BuildRequires: git python-srpm-macros
Requires:       python27

%include /usr/lib/rpm/macros.d/macros.python
%description
Easily download, build, install, upgrade, and uninstall Python packages

%setup -q -c -T                                                                                                                                                  
 
%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

DIR=`ls $RPM_BUILD_DIR | grep setuptools`
chmod -R u+w %{_builddir}/%{name}-%{version}

%build
cd $RPM_BUILD_DIR/%{name}-%{version}
%{__python} setup.py build

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
#cd $RPM_BUILD_DIR/$DIR
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
