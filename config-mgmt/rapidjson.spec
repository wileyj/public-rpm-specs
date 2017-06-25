%define repo https://github.com/miloyip/rapidjson
%define gitversion %(echo `curl -s  %{repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-targetv">'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 10
%define alt_name RapidJSON
Name:           rapidjson
Version:        %{gitversion}
Release:        %{rel_version}.%{revision}.%{dist}
Summary:        A fast JSON parser/generator for C++ with both SAX/DOM style API
Group:          System Environment/Base
License:        ASL 2.0
Vendor: 	%{vendor}
Packager: 	%{packager}
URL:            %{repo}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gcc-c++ make cmake doxygen

%description
RapidJSON is a JSON parser and generator for C++. It was inspired by RapidXml.
RapidJSON is small but complete. It supports both SAX and DOM style API. The SAX parser is only a half thousand lines of code.
RapidJSON is fast. Its performance can be comparable to strlen(). It also optionally supports SSE2/SSE4.2 for acceleration.
RapidJSON is self-contained and header-only. It does not depend on external libraries such as BOOST. It even does not depend on STL.
RapidJSON is memory-friendly. Each JSON value occupies exactly 16 bytes for most 32/64-bit machines (excluding text string). By default it uses a fast memory allocator, and the parser allocates memory compactly during parsing.
RapidJSON is Unicode-friendly. It supports UTF-8, UTF-16, UTF-32 (LE & BE), and their detection, validation and transcoding internally. For example, you can read a UTF-8 file and let RapidJSON transcode the JSON strings into UTF-16 in the DOM. It also supports surrogates and "\u0000" (null character).

%package -n %{name}-devel
Summary:        %{summary}¬
Group:          Development/Languages¬
Requires:	%{name}

%description -n %{name}-devel
%{name}-devel package 

%package -n %{name}-docs
Summary:        %{summary}¬
Group:          Development/Languages¬
Requires:       %{name}

%description -n %{name}-docs
%{name}-docs package

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
if [ -d %{buildroot} ]; then
    rm -rf %{buildroot}
fi

git clone %{repo} %{name}-%{version}
cd %{name}-%{version}

%build
cd %{name}-%{version}

%install
cd %{name}-%{version}
rm -rf %{buildroot}
%__mkdir_p release
pwd
cd release
export CLASSPATH="$CLASSPATH"
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ..
make DESTDIR=%{buildroot} INSTALL="install -p" install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}


%files
%{_prefix}/lib/cmake/*
%{_prefix}/lib/pkgconfig/*
%files -n %{name}-devel
%{_includedir}/%{name}/*

%files -n %{name}-docs
%{_docdir}/%{alt_name}/*

%changelog
