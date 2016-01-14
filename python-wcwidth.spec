%define pkgname wcwidth
%define pip_version %(echo `curl -s https://pypi.python.org/pypi/%{pkgname} | grep "<title>" | awk '{print $2}'`)
%define filelist %{pkgname}-%{version}-filelist

Name:           python-%{pkgname}
Version:        %{pip_version}
Release:        1.%{dist}
Summary:        a Terminal Emulator
Group:          Development/Languages
License:        BSD
Packager:       %{packager}
Vendor:         %{vendor}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python, python-devel, python-setuptools
Requires:       python
%{?load: %{_rpmconfigdir}/macros.d/macros.python}

%description
This Library is mainly for those implementing a Terminal Emulator, or programs that carefully produce output to be interpreted by one.

Problem Statement: When printed to the screen, the length of the string is usually equal to the number of cells it occupies. However, there are categories of characters that occupy 2 cells (full-wide), and others that occupy 0.

Solution: POSIX.1-2001 and POSIX.1-2008 conforming systems provide wcwidth(3) and wcswidth(3) C functions of which this python module’s functions precisely copy. These functions return the number of cells a unicode string is expected to occupy.

This library aims to be forward-looking, portable, and most correct. The most current release of this API is based on the Unicode Standard release files:

EastAsianWidth-8.0.0.txt
2015-02-10, 21:00:00 GMT [KW, LI]
DerivedGeneralCategory-8.0.0.txt
2015-02-13, 13:47:11 GMT [MD]

%prep
curl -o $RPM_SOURCE_DIR/%{name}.tar.gz `curl -s https://pypi.python.org/pypi/python-%{pkgname} | grep tar.gz | cut -d '"' -f2 | cut -f1 -d "#"`
tar -xzvf $RPM_SOURCE_DIR/%{name}.tar.gz 
chmod -R u+w %{_builddir}/python_%{pkgname}-%{version}

%build
cd $RPM_BUILD_DIR/python_%{pkgname}-%{version}
%{__python} setup.py build

%install
cd $RPM_BUILD_DIR/python_%{pkgname}-%{version}
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

%files -f python_%{pkgname}-%{pip_version}/%filelist
%defattr(-,root,root)

%changelog