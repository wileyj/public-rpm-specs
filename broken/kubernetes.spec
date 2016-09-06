%global vendorname kubernetes
%define url https://github.com/kubernetes/kubernetes
%define gitversion %(echo `curl -s %{url}/releases | grep 'class="tag-name"' | head -1 |  tr -d '\\-</span class="tag-name">'`)
%define repo %{url}.git
%define release_ver 1
%global _python_bytecompile_errors_terminate_build 0

Name:           %{vendorname}
Version:        %{gitversion}
Release:        %{release_ver}.%{dist}
Summary:        %{_summary}
License:        Go License
Vendor:         %{vendor}
Packager:       %{packager}

BuildRequires:  git golang >= 1.5.0
Requires:       golang >= 1.5.0
Provides:       golang-%{provider}
Provides:       golang(%{import_path}) = %{version}-%{release}

%include %{_rpmconfigdir}/macros.d/macros.golang
%description
%{summary}


%prep
#if [ -d %{name}-%{version} ];then
#    rm -rf %{name}-%{version}
#fi
#git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
#git submodule init
#git submodule update

%build
export GOPATH=%{buildroot}%{gopath}
cd %{name}-%{version}
source /etc/profile.d/golang.sh
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" CC="gcc" CC_FOR_TARGET="gcc" GOOS=linux \
#GOARCH=%{gohostarch} ./make.bash --no-clean
#GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -buildmode=shared std

export CFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_"
%{__make} %{?_smp_mflags}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{name}-%{version}-filelist" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%changelog

