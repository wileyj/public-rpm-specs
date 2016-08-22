%define have_systemd  0

Name:           erlang
Version:        18.0.3
Release:        8.1.%{dist}
Summary:        General-purpose programming language and runtime environment
License:        Apache-2.0
Group:          Development/Languages/Other
Url:            http://www.erlang.org
Source0:        https://github.com/erlang/otp/archive/OTP-%{version}.tar.gz
Source3:        %{name}-rpmlintrc
Source4:        epmd.init
Source5:        erlang.sysconfig
Source6:        macros.erlang
Source7:        epmd.service
Source8:        epmd.socket
Patch0:         otp-R16B-rpath.patch
Patch4:         erlang-not-install-misc.patch
Patch5:         crypto.patch
Patch6:         erts_fix_unlock_status_lock.patch
BuildRequires:  autoconf
BuildRequires:  gcc-c++
BuildRequires:  ncurses-devel
BuildRequires:  openssh
BuildRequires:  openssl-devel
BuildRequires:  tcl-devel
BuildRequires:  unixODBC-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  jdk
BuildRequires:  krb5-devel
#BuildRequires:  xsltproc
BuildRequires:  libxslt
Requires:       erlang-epmd

%define epmd_home %{_var}/lib/epmd

%description
Erlang is a general-purpose programming language and runtime
environment. Erlang has built-in support for concurrency, distribution
and fault tolerance. Erlang is used in several large telecommunication
systems from Ericsson.

%package debugger
Summary:        A debugger for debugging and testing of Erlang programs
Group:          Development/Languages/Other
Requires:       %{name} = %{version}
Requires:       %{name}-gs = %{version}

%description debugger
A debugger for debugging and testing of Erlang programs.

%package dialyzer
Summary:        A DIscrepany AnaLYZer for ERlang programs
Group:          Development/Languages/Other
Requires:       %{name} = %{version}
Requires:       %{name}-gs = %{version}
Requires:       graphviz

%description dialyzer
A DIscrepany AnaLYZer for ERlang programs.

%package doc
Summary:        Erlang documentation
Group:          Development/Languages/Other
%if 0%{?suse_version}
Recommends:     %{name} = %{version}
%endif

%description doc
Documentation for Erlang.

%package epmd
Summary:        Erlang Port Mapper daemon
Group:          Development/Languages/Other
Requires:       %{name} = %{version}

%description epmd
The Erlang Port Mapper daemon acts as a name server on all hosts involved in distributed Erlang computations.

%package et
Summary:        An event tracer for Erlang programs
Group:          Development/Languages/Other
Requires:       %{name} = %{version}
Requires:       %{name}-gs = %{version}

%description et
An event tracer for Erlang programs.

%package jinterface
Summary:        Erlang Java Interface
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}
Requires:       java >= 1.5.0

%description jinterface
JInterface module for accessing erlang from Java

%package gs
Summary:        A library for Tcl/Tk support in Erlang
Group:          Development/Languages/Other
Requires:       %{name} = %{version}
Requires:       tk

%description gs
A Graphics System used to write platform independent user interfaces.

%package reltool
Summary:        A release management tool
Group:          Development/Languages/Other
Requires:       %{name} = %{version}
Requires:       %{name}-gs = %{version}

%description reltool
Reltool is a release management tool. It analyses a given
Erlang/OTP installation and determines various dependencies
between applications. The graphical frontend depicts the
dependencies and enables interactive customization of a
target system. The backend provides a batch interface
for generation of customized target systems.

%package observer
Summary:        A GUI tool for observing an erlang system
Group:          Development/Languages/Other
Requires:       %{name} = %{version}

%description observer
The observer is gui frontend containing various tools to inspect a system.
It displays system information, application structures, process information,
ets or mnesia tables and a frontend for tracing with ttb. 

%package src
Summary:        Erlang/OTP applications sources
Group:          Development/Languages/Other
Requires:       %{name} = %{version}

%description src
Erlang sources for all the applications in the Erlang/OTP system.
They are useful for educational purpose and as a base for creating
embedded systems.

%package debugger-src
Summary:        Erlang/OTP debugger application sources
Group:          Development/Languages/Other
Requires:       %{name}-debugger = %{version}

%description debugger-src
Erlang sources for the debugger application in the Erlang/OTP system.
They are useful for educational purpose and as a base for creating
embedded systems.

%package dialyzer-src
Summary:        Erlang/OTP dialyzer application sources
Group:          Development/Languages/Other
Requires:       %{name}-dialyzer = %{version}

%description dialyzer-src
Erlang sources for the dialyzer application in the Erlang/OTP system.
They are useful for educational purpose and as a base for creating
embedded systems.

%package et-src
Summary:        Erlang/OTP et application sources
Group:          Development/Languages/Other
Requires:       %{name}-et = %{version}

%description et-src
Erlang sources for the et application in the Erlang/OTP system.
They are useful for educational purpose and as a base for creating
embedded systems.

%package gs-src
Summary:        Erlang/OTP gs application sources
Group:          Development/Languages/Other
Requires:       %{name}-gs = %{version}

%description gs-src
Erlang sources for the gs application in the Erlang/OTP system.
They are useful for educational purpose and as a base for creating
embedded systems.

%package jinterface-src
Summary:        Erlang/OTP jinterface application sources
Group:          Development/Languages/Other
Requires:       %{name}-jinterface = %{version}

%description jinterface-src
Erlang sources for the jinterface application in the Erlang/OTP system.
They are useful for educational purpose and as a base for creating
embedded systems.

%package reltool-src
Summary:        Erlang/OTP reltool application sources
Group:          Development/Languages/Other
Requires:       %{name}-reltool = %{version}

%description reltool-src
Erlang sources for the reltool application in the Erlang/OTP system.
They are useful for educational purpose and as a base for creating
embedded systems.

%package observer-src
Summary:        Erlang/OTP observer application sources
Group:          Development/Languages/Other
Requires:       %{name}-observer = %{version}

%description observer-src
Erlang sources for the observer application in the Erlang/OTP system.
They are useful for educational purpose and as a base for creating embedded systems.

%prep
%setup -q -n otp-OTP-%{version}
%patch0 -p1 -b .rpath
%patch4 -p1
%patch5 -p1
%patch6 -p1

./otp_build autoconf
# enable dynamic linking for ssl
sed -i 's|SSL_DYNAMIC_ONLY=no|SSL_DYNAMIC_ONLY=yes|' erts/configure
# Remove shipped zlib sources
#rm -f erts/emulator/zlib/*.[ch]


%build
# we need build only 1.5 target for java
# for SLE only
%if 0%{?sles_version} >= 10 || 0%{?suse_version} >= 1110
	export JAVAC="javac -source 1.5 -target 1.5"
%endif
%if 0%{?suse_version} == 1100 || 0%{?fedora_version} == 9
export CFLAGS="-fno-strict-aliasing"
%else
export CFLAGS="%{optflags} -fno-strict-aliasing"
%endif
export CXXFLAGS=$CFLAGS

%configure \
    --with-ssl=%{_prefix} \
    --enable-threads \
    --enable-smp-support \
    --enable-kernel-poll \
    --enable-hipe \
    --enable-shared-zlib
make %{?_smp_mflags} clean
make %{?_smp_mflags}
PATH=$PWD/bin:$PATH make %{?_smp_mflags} docs

%install
%if 0%{?sles_version} >= 10
    make DESTDIR=%{buildroot} install
    make DESTDIR=%{buildroot} install-docs
%else
    %make_install install-docs
%endif

export TOOLS_VERSION=`ls %{buildroot}%{_libdir}/erlang/lib/ |grep ^tools- | sed "s|tools-||"`

# clean up
find %{buildroot}%{_libdir}/erlang -perm 0775 | xargs chmod -v 0755
find %{buildroot}%{_libdir}/erlang -name Makefile | xargs chmod -v 0644
find %{buildroot}%{_libdir}/erlang -name \*.bat | xargs rm -fv
find %{buildroot}%{_libdir}/erlang -name index.txt.old | xargs rm -fv
rm %{buildroot}%{_libdir}/erlang/lib/tools-$TOOLS_VERSION/emacs/test.erl.orig
mv %{buildroot}%{_libdir}/erlang/lib/tools-$TOOLS_VERSION/emacs/test.erl.indented %{buildroot}%{_libdir}/erlang/lib/tools-$TOOLS_VERSION/emacs/test.erl

mv README.md README
mkdir -p erlang_doc
find %{buildroot}%{_libdir}/erlang -maxdepth 3 -type d -name doc -or -name info | while read S;do D=`echo $S | sed -e 's|%{buildroot}%{_libdir}/erlang|erlang_doc|'`; B=`dirname $D`; mkdir -p $B; mv $S $D; done
find %{buildroot}%{_libdir}/erlang/man -type f -exec gzip {} +

mkdir -p %{buildroot}%{_javadir}
cd %{buildroot}%{_javadir}
export JINTERFACE_VERSION=`ls %{buildroot}%{_libdir}/erlang/lib/ |grep ^jinterface- | sed "s|jinterface-||"`
ln -sf ../../%{_lib}/erlang/lib/jinterface-$JINTERFACE_VERSION/priv/OtpErlang.jar OtpErlang-$JINTERFACE_VERSION.jar
cd -

rm -r %{buildroot}%{_libdir}/erlang/lib/diameter-*
rm -r %{buildroot}%{_libdir}/erlang/man/man?/diameter* # Doesn't make much sense w/o the above
rm -r lib/diameter lib/xmerl/test/xmerl_xsd_SUITE_data # Can't distribute either source
mkdir -p %{buildroot}%{_mandir}/man1
for link in $(ls %{buildroot}%{_libdir}/erlang/man/man1/); do
    ln -s %{_libdir}/erlang/man/man1/$link %{buildroot}%{_mandir}/man1/$link
done
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp
cat > %{buildroot}%{_datadir}/emacs/site-lisp/erlang.el << EOF
(setq load-path (cons "%{_libdir}/erlang/lib/tools-$TOOLS_VERSION/emacs" load-path))
(add-to-list 'load-path "%{_datadir}/emacs/site-lisp/ess")
(load-library "erlang-start")
EOF

#find . -name "start_erl*" | xargs chmod 755
#%fdupes %{buildroot}/%{_libdir}/erlang
#%fdupes -s erlang_doc

install -d -m 0750        %{buildroot}%{epmd_home}
install -d -m 0755        %{buildroot}%{_sbindir}
%if 0%{?have_systemd}
install -D -m 0644 %{S:7} %{buildroot}%{_unitdir}/epmd.service
install -D -m 0644 %{S:8} %{buildroot}%{_unitdir}/epmd.socket
ln -s   /sbin/service     %{buildroot}%{_sbindir}/rcepmd
%else
ln -s   /etc/init.d/epmd  %{buildroot}%{_sbindir}/rcepmd
%endif
install -D -m 0755 %{S:4} %{buildroot}/etc/init.d/epmd
install -D -m 0644 %{S:5} %{buildroot}/var/adm/fillup-templates/sysconfig.erlang
install -D -m 0644 %{S:6} %{buildroot}%{_sysconfdir}/rpm/macros.erlang

if [ -d "%{buildroot}%{_libdir}/%{name}/lib/wx-1.4" ];then
    rm -rf %{buildroot}%{_libdir}/%{name}/lib/wx-1.4
fi

%pre epmd
/usr/sbin/groupadd -r epmd >/dev/null 2>&1 || :
/usr/sbin/useradd -g epmd -s /bin/false -r -c "Erlang Port Mapper Daemon" -d %{epmd_home} epmd >/dev/null 2>&1 || :
%if 0%{?have_systemd}
%service_add_pre epmd.service epmd.socket
%endif

%post epmd
%fillup_only erlang
%if 0%{?have_systemd}
%service_add_post epmd.service epmd.socket
%endif

%preun epmd
%if 0%{?have_systemd}
%service_del_preun epmd.service epmd.socket
%endif
%stop_on_removal epmd

%postun epmd
%if 0%{?have_systemd}
%service_del_postun epmd.service epmd.socket
%endif
%restart_on_update epmd
%{insserv_cleanup}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE.txt README
%if 0%{?have_systemd}
%endif
%doc %{_libdir}/erlang/PR.template
%doc %{_libdir}/erlang/README
%doc %{_libdir}/erlang/COPYRIGHT
%{_bindir}/*
%exclude %{_bindir}/dialyzer
%exclude %{_bindir}/epmd
%dir %{_libdir}/erlang
%dir %{_libdir}/erlang/lib/
%exclude %{_libdir}/erlang/lib/*/src
%exclude %{_libdir}/erlang/lib/*/c_src
%exclude %{_libdir}/erlang/lib/*/java_src
%{_libdir}/erlang/bin/
%exclude %{_libdir}/erlang/bin/dialyzer
%exclude %{_libdir}/erlang/bin/epmd
%{_libdir}/erlang/erts-*/
%exclude %{_libdir}/erlang/erts-*/bin/dialyzer
%exclude %{_libdir}/erlang/erts-*/bin/epmd
%{_libdir}/erlang/lib/asn1-*/
%{_libdir}/erlang/lib/common_test-*/
%{_libdir}/erlang/lib/compiler-*/
%{_libdir}/erlang/lib/cosEvent-*/
%{_libdir}/erlang/lib/cosEventDomain-*/
%{_libdir}/erlang/lib/cosFileTransfer-*/
%{_libdir}/erlang/lib/cosNotification-*/
%{_libdir}/erlang/lib/cosProperty-*/
%{_libdir}/erlang/lib/cosTime-*/
%{_libdir}/erlang/lib/cosTransactions-*/
%{_libdir}/erlang/lib/crypto-*/
%{_libdir}/erlang/lib/edoc-*/
%{_libdir}/erlang/lib/eldap-*/
%{_libdir}/erlang/lib/erl_docgen-*/
%{_libdir}/erlang/lib/erl_interface-*/
%{_libdir}/erlang/lib/erts-*/
%{_libdir}/erlang/lib/eunit-*/
%{_libdir}/erlang/lib/hipe-*/
%{_libdir}/erlang/lib/ic-*/
%{_libdir}/erlang/lib/inets-*/
%{_libdir}/erlang/lib/kernel-*/
%{_libdir}/erlang/lib/megaco-*/
%{_libdir}/erlang/lib/mnesia-*/
%{_libdir}/erlang/lib/odbc-*/
%{_libdir}/erlang/lib/orber-*/
%{_libdir}/erlang/lib/os_mon-*/
%{_libdir}/erlang/lib/ose-*/
%{_libdir}/erlang/lib/otp_mibs-*/
%{_libdir}/erlang/lib/parsetools-*/
%{_libdir}/erlang/lib/percept-*/
%{_libdir}/erlang/lib/public_key-*/
%{_libdir}/erlang/lib/runtime_tools-*/
%{_libdir}/erlang/lib/sasl-*/
%{_libdir}/erlang/lib/snmp-*/
%{_libdir}/erlang/lib/ssh-*/
%{_libdir}/erlang/lib/ssl-*/
%{_libdir}/erlang/lib/stdlib-*/
%{_libdir}/erlang/lib/syntax_tools-*/
%{_libdir}/erlang/lib/test_server-*/
%{_libdir}/erlang/lib/tools-*/
%{_libdir}/erlang/lib/typer-*/
%{_libdir}/erlang/lib/webtool-*/
%{_libdir}/erlang/lib/xmerl-*/
%{_libdir}/erlang/man/
%{_mandir}/man1/*.1.gz
%{_libdir}/erlang/releases/
%{_libdir}/erlang/usr/
%{_libdir}/erlang/Install
%{_datadir}/emacs/site-lisp/erlang.el
%config %{_sysconfdir}/rpm/macros.erlang

%files debugger
%defattr(-,root,root)
%{_libdir}/erlang/lib/debugger-*/
%exclude %{_libdir}/erlang/lib/debugger-*/src

%files dialyzer
%defattr(-,root,root)
%{_libdir}/erlang/lib/dialyzer-*/
%exclude %{_libdir}/erlang/lib/dialyzer-*/src
%{_bindir}/dialyzer
%{_libdir}/erlang/bin/dialyzer
%{_libdir}/erlang/erts-*/bin/dialyzer

%files doc
%defattr(0644,root,root,0755)
%doc erlang_doc/*

%files et
%defattr(-,root,root)
%{_libdir}/erlang/lib/et-*/
%exclude %{_libdir}/erlang/lib/et-*/src

%files epmd
%defattr(-,root,root)
%{_bindir}/epmd
%{_libdir}/erlang/bin/epmd
%{_libdir}/erlang/erts-*/bin/epmd
%dir %attr(-,epmd,epmd) %{epmd_home}
%if 0%{?have_systemd}
%{_unitdir}/epmd.service
%{_unitdir}/epmd.socket
%endif
/etc/init.d/epmd
%{_sbindir}/rcepmd
/var/adm/fillup-templates/sysconfig.erlang

%files gs
%defattr(-,root,root)
%{_libdir}/erlang/lib/gs-*/
%exclude %{_libdir}/erlang/lib/gs-*/src

%files jinterface
%defattr(-,root,root,-)
%{_libdir}/erlang/lib/jinterface-*/
%exclude %{_libdir}/erlang/lib/jinterface-*/java_src
%{_javadir}/*

%files reltool
%defattr(-,root,root)
%{_libdir}/erlang/lib/reltool-*/
%exclude %{_libdir}/erlang/lib/reltool-*/src

%files observer
%defattr(-,root,root)
%{_libdir}/erlang/lib/observer-*/
%exclude %{_libdir}/erlang/lib/observer-*/src

%files src
%defattr(-,root,root)
%exclude %{_libdir}/erlang/lib/erl_interface-*/src/INSTALL
%{_libdir}/erlang/lib/*/src
%{_libdir}/erlang/lib/*/c_src
%{_libdir}/erlang/lib/*/java_src
%exclude %{_libdir}/erlang/lib/debugger-*/src
%exclude %{_libdir}/erlang/lib/dialyzer-*/src
%exclude %{_libdir}/erlang/lib/et-*/src
%exclude %{_libdir}/erlang/lib/gs-*/src
%exclude %{_libdir}/erlang/lib/jinterface-*/java_src
%exclude %{_libdir}/erlang/lib/reltool-*/src
%exclude %{_libdir}/erlang/lib/observer-*/src

%files debugger-src
%defattr(-,root,root)
%{_libdir}/erlang/lib/debugger-*/src

%files dialyzer-src
%defattr(-,root,root)
%{_libdir}/erlang/lib/dialyzer-*/src

%files et-src
%defattr(-,root,root)
%{_libdir}/erlang/lib/et-*/src

%files gs-src
%defattr(-,root,root)
%{_libdir}/erlang/lib/gs-*/src

%files jinterface-src
%defattr(-,root,root)
%{_libdir}/erlang/lib/jinterface-*/java_src

%files reltool-src
%defattr(-,root,root)
%{_libdir}/erlang/lib/reltool-*/src

%files observer-src
%defattr(-,root,root)
%{_libdir}/erlang/lib/observer-*/src


%changelog
