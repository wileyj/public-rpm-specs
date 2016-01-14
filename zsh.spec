# this file is encoded in UTF-8  -*- coding: utf-8 -*-

Summary: Powerful interactive shell
Name: zsh
Version: 5.0.8
Release: 3%{?dist}
License: MIT
URL: http://zsh.sourceforge.net/
Group: System Environment/Shells
Source0: http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1: zlogin.rhs
Source2: zlogout.rhs
Source3: zprofile.rhs
Source4: zshrc.rhs
Source5: zshenv.rhs
Source6: dotzshrc
Source7: zshprompt.pl

# legacy downstream patches, TODO: either get them upstream or drop them
Patch0: zsh-serial.patch
Patch1: zsh-4.3.6-8bit-prompts.patch
Patch2: zsh-test-C02-dev_fd-mock.patch

# backport completion-related upstream fixes (#1238544)
Patch3: zsh-5.0.8-comp-bz1238544.patch

BuildRequires: coreutils sed ncurses-devel libcap-devel
BuildRequires: texinfo texi2html gawk net-tools
Requires(post): info grep
Requires(preun): info
Requires(postun): coreutils grep

Provides: /bin/zsh

%description
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

%package html
Summary: Zsh shell manual in html format
Group: System Environment/Shells

%description html
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

This package contains the Zsh manual in html format.

%prep

%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp -p %SOURCE7 .

%build
# Avoid stripping...
export LDFLAGS=""
%configure --enable-etcdir=%{_sysconfdir} --with-tcsetpgrp  --disable-maildir-support --disable-dynamic --disable-dynamic-nss --disable-docs

make all html

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall install.info \
  fndir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/functions \
  sitefndir=$RPM_BUILD_ROOT%{_datadir}/%{name}/site-functions \
  scriptdir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/scripts \
  sitescriptdir=$RPM_BUILD_ROOT%{_datadir}/%{name}/scripts \
  runhelpdir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/help

rm -f ${RPM_BUILD_ROOT}%{_bindir}/zsh-%{version}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
for i in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5}; do
    install -m 644 $i $RPM_BUILD_ROOT%{_sysconfdir}/"$(basename $i .rhs)"
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/skel
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.zshrc

# This is just here to shut up rpmlint, and is very annoying.
# Note that we can't chmod everything as then rpmlint will complain about
# those without a she-bang line.
for i in checkmail harden run-help zcalc zkbd; do
    sed -i -e 's!/usr/local/bin/zsh!%{_bindir}/zsh!' \
    $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/$i
    chmod +x $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/$i
done

sed -i "s!$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/help!%{_datadir}/%{name}/%{version}/help!" \
    $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/{run-help,_run-help}

%__cp ${RPM_BUILD_ROOT}%{_bindir}/zsh ${RPM_BUILD_ROOT}%{_bindir}/rzsh

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
    echo "%{_bindir}/r%{name}" >> %{_sysconfdir}/shells
  else
    grep -q "^%{_bindir}/%{name}$" %{_sysconfdir}/shells || echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
    grep -q "^%{_bindir}/r%{name}$" %{_sysconfdir}/shells || echo "%{_bindir}/r%{name}" >> %{_sysconfdir}/shells
  fi
fi

if [ -f %{_infodir}/zsh.info.gz ]; then
# This is needed so that --excludedocs works.
/sbin/install-info %{_infodir}/zsh.info.gz %{_infodir}/dir \
  --entry="* zsh: (zsh).			An enhanced bourne shell."
fi

%preun
if [ "$1" = 0 ] ; then
    if [ -f %{_infodir}/zsh.info.gz ]; then
    # This is needed so that --excludedocs works.
    /sbin/install-info --delete %{_infodir}/zsh.info.gz %{_infodir}/dir \
      --entry="* zsh: (zsh).			An enhanced bourne shell."
    fi
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
        TmpFile=`%{_bindir}/mktemp /tmp/.zshrpmXXXXXX`
        grep -v '^%{_bindir}/zsh$' %{_sysconfdir}/shells > $TmpFile
        cp -f $TmpFile %{_sysconfdir}/shells
        rm -f $TmpFile
   	sed -i '\!^%{_bindir}/%{name}$!d' %{_sysconfdir}/shells
	sed -i '\!^/bin/%{name}$!d' %{_sysconfdir}/shells
fi

%files
%defattr(-,root,root)
%doc README LICENCE Etc/BUGS Etc/CONTRIBUTORS Etc/FAQ FEATURES MACHINES
%doc NEWS Etc/zsh-development-guide Etc/completion-style-guide zshprompt.pl
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/*/*
%{_infodir}/*
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/skel/.z*
%config(noreplace) %{_sysconfdir}/z*
%{_bindir}/r%{name}

%files html
%defattr(-,root,root)
%doc Doc/*.html

%changelog
