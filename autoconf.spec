Summary:	A GNU tool for automatically configuring source code.
Name:		autoconf
Version:	2.69
Release:	1.%{dist}
License:	GPL
Vendor: %{vendor}
Packager: %{packager}
Group:		Development/Tools
Source:		http://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.gz
Patch0:     	autoconf-2.59-intrinsic.patch
Patch1:		autoconf-2.59-lock.patch
URL:		http://www.gnu.org/software/autoconf/
BuildRequires:	sed, m4, emacs
Requires:	gawk, m4, mktemp, perl, textutils, imake
BuildRequires: 	help2man
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-root
AutoProv:   	0
AutoReq:    	0
%if 0%{?el5}
Provides:   	autoconf269
obsoletes:  	autoconf261
%endif

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%setup -q -n autoconf-%{version}
#%patch0 -p1 -b .mod-x
#%patch1 -p1 -b .lock

%build
%configure
make

#check
#make check VERBOSE=yes

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post
/sbin/install-info %{_infodir}/autoconf.info.gz %{_infodir}/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --del %{_infodir}/autoconf.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
%{_datadir}/autoconf
%{_datadir}/emacs/site-lisp
%{_mandir}/man1/*
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO

%changelog
