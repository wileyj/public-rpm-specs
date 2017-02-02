%global __os_install_post %{nil}
%define repo https://github.com/postmodern/chruby
%define gitversion %(echo `curl -s https://github.com/postmodern/chruby/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">v'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1 | cut -c1-7`)
%define rel_version 1

Name:		chruby
Version:	%{gitversion}
Release: %{rel_version}.%{revision}.%{dist}
Summary:	Changes the current Ruby.
Group:		System/Applications
License:	MIT
URL:		https://github.com/postmodern/chruby
BuildArch:	noarch
BuildRequires: 	make ruby-rpm-macros rubygem-rpm-macros
Provides:       chruby = %{version}
Requires:	ruby rubygems ruby-install ruby
%description
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

%files -n %{name}-docs
%dir /usr/local/share/doc/%{name}-%{version}
/usr/local/share/doc/%{name}-%{version}/*


