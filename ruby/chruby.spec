%define repo https://github.com/postmodern/chruby
%define gitversion %(echo `curl -s https://github.com/postmodern/chruby/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)


Name:		chruby
Version:	%{gitversion}
Release:	1.%{?dist}
Summary:	Changes the current Ruby.
Group:		System/Applications
License:	MIT
URL:		https://github.com/postmodern/chruby
BuildArch:	noarch
BuildRequires: 	make
Source4:	macros.ruby
Source5:	macros.rubygems
Provides:       chruby = %{version}
Requires:	ruby rubygems ruby-install ruby
%description
%{summary}

%package devel
Summary:    A Ruby development environment for chruby
Group:      Development/Languages
License:    Ruby or BSD
Requires:   chruby = %{version} ruby-install ruby-build ruby ruby-devel
Provides:   chruby-devel = %{version}
Obsoletes:  rubygems-devel

%description devel
%{summary}

%package docs
Summary:    Docs for chruby
Group:      Development/Libraries
License:    Ruby or BSD
Requires:   chruby = %{version}
Provides:   chruby-docs = %{version}

%description docs
%{summary}


%prep

if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
#cd %{name}-%{version}
#%{__make}

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=%{buildroot}

%{__mkdir_p} %{buildroot}/etc/profile.d
%{__mkdir_p} %{buildroot}/opt/rubies
%{__mkdir_p} %{buildroot}%{_bindir}
%__ln_s /usr/local/bin/%{name}-exec  %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE4} %{buildroot}%{_rpmconfigdir}/macros.d/macros.ruby
sed -i "s/%ruby/ruby/" %{buildroot}%{_rpmconfigdir}/macros.d/macros.ruby
install -m 644 %{SOURCE5} %{buildroot}%{_rpmconfigdir}/macros.d/macros.rubygems
sed -i "s/%ruby/ruby/" %{buildroot}%{_rpmconfigdir}/macros.d/macros.rubygems

cat <<EOF> %{buildroot}/etc/profile.d/chruby.sh
if [ -n "$BASH_VERSION" ] || [ -n "$ZSH_VERSION" ]; then
  source /usr/local/share/chruby/chruby.sh
fi
EOF

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}




%files -n %{name}
%defattr(-,root,root,-)
%dir /opt/rubies
%{_bindir}/%{name}
%attr(0755,root,root) /usr/local/share/chruby/auto.sh
%attr(0755,root,root) /usr/local/share/chruby/chruby.sh
%{_sysconfdir}/profile.d/%{name}.sh
/usr/local/bin/%{name}-exec

%files -n %{name}-devel
%{_rpmconfigdir}/macros.d/macros.ruby
%{_rpmconfigdir}/macros.d/macros.rubygems

%files -n %{name}-docs
%dir /usr/local/share/doc/%{name}-%{version}
/usr/local/share/doc/%{name}-%{version}/*


