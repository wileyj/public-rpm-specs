
Name:		cpulimit
Version:	0.2
Release:	1.%{dist}
Summary:	limits the CPU usage of a process
License:	GPLv3+
Vendor: 	%{vendor}
Packager: 	%{packager}
Group:		Applications/System
URL:		https://github.com/opsengine/cpulimit
BuildArch:	x86_64
Source0:	cpulimit.tar.gz

BuildRequires:	clang
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Cpulimit is a tool which limits the CPU usage of a process (expressed in percentage, not in CPU time). It is useful to control batch jobs, when you don't want them to eat too many CPU cycles. The goal is prevent a process from running for more than a specified time ratio. It does not change the nice value or other scheduling priority settings, but the real CPU usage. Also, it is able to adapt itself to the overall system load, dynamically and quickly. The control of the used CPU amount is done sending SIGSTOP and SIGCONT POSIX signals to processes. All the children processes and threads of the specified process will share the same percentage of CPU.

%prep 

%setup -q -n %{name}

%build
git pull 

make %{?_smp_mflags}

%install
%__mkdir_p %{buildroot}%{_bindir}
install -m 0755 src/cpulimit %{buildroot}%{_bindir}/%{name}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%{_bindir}/%{name}
%changelog
