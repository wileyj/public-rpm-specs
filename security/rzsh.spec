Name:           rzsh
Summary:        rzsh metapackage
Version:        1.0.0
Release:	     1.%{dist}
License: MIT
Group: System Environment/Shells
Requires(post): zsh
BuildArch: noarch

%description
%{summary}

%post
%__cp -a /bin/zsh /bin/rzsh 

%postun
rm -f /bin/rzsh 


%files



