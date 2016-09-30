%define repo https://github.com/rbenv/ruby-build
%define gitversion %(echo `curl -s https://github.com/rbenv/ruby-build/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">v'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1 | cut -c1-7`)
%define rel_version 1

%define rbenv /opt/rbenv

Name:		ruby-build
Version:	%{gitversion}
Release: %{rel_version}.%{revision}.%{dist}
Summary:	builds ruby for rbenv/chruby
Group:		System/Applications
License:	MIT
URL:		https://github.com/rbenv/ruby-build
BuildArch:	noarch
Provides:       %{name} = %{version}
Requires:	rbenv

%description
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

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT

BIN_PATH="${PREFIX}/bin"
SHARE_PATH="${PREFIX}/share/ruby-build"

mkdir -p "$BIN_PATH" "$SHARE_PATH"
mkdir -p %{buildroot}%{rbenv}/rubies

install -p bin/* "$BIN_PATH"
install -p -m 0644 share/ruby-build/* "$SHARE_PATH"


%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}/usr/local/bin
install -Dp -m0755 bin/rbenv-install %{buildroot}/usr/local/bin/rbenv-install
install -Dp -m0755 bin/rbenv-uninstall %{buildroot}/usr/local/bin/rbenv-uninstall
install -Dp -m0755 bin/ruby-build %{buildroot}/usr/local/bin/ruby-build

%__ln_s /usr/local/bin/rbenv-install %{buildroot}%{_bindir}/rbenv-install
%__ln_s /usr/local/bin/rbenv-uninstall %{buildroot}%{_bindir}/rbenv-uninstall
%__ln_s /usr/local/bin/ruby-build %{buildroot}%{_bindir}/ruby-build

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}




%files 
%defattr(-,root,root,-)
%{_bindir}/rbenv-install
%{_bindir}/rbenv-uninstall
%{_bindir}/ruby-build
%{rbenv}/rubies
%attr(0755,root,root) /usr/local/bin/rbenv-install
%attr(0755,root,root) /usr/local/bin/rbenv-uninstall
%attr(0755,root,root) /usr/local/bin/ruby-build

