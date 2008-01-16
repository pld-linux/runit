Summary:	a UNIX init scheme with service supervision
Name:		runit
Version:	1.7.2
Release:	0.1
License:	BSD style
Group:		Daemons
URL:		http://smarden.org/runit/
Source0:	http://smarden.org/runit/%{name}-%{version}.tar.gz
# Source0-md5:	35448e97188544914f298c88871ab984
#Source1:	%{name}.svup
#Source2:	%{name}.svdown
#Source3:	%{name}.svdepcalc
#Source4:	%{name}.dependencies.README
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
runit is a daemontools alike replacement for sysvinit and other init
schemes. runit runs on GNU/Linux, OpenBSD, FreeBSD, and can easily be
adapted to other unix operating systems. If runit runs for you on any
other operating system or Linux distribution, please let me know.

Warning: Replacing sysvinit or init can cause the system's boot to
fail. Make sure you are able to recover and repair your system, for
example if you run a boot loader, it should be able to pass
init=/bin/sh to the kernel.

%prep
%setup -qc
mv admin/%{name}-%{version}/* .

%build
echo '%{__cc} %{rpmldflags}' > src/conf-ld
echo '%{__cc] %{rpmcflags} -Wall' > src/conf-cc
./package/compile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} command/svisup
install %{SOURCE2} command/svisdown
install %{SOURCE3} command/svdepcalc
install %{SOURCE4} doc/dependencies.README
for i in $(cat package/commands) svisup svisdown svdepcalc; do
	install command/$i $RPM_BUILD_ROOT%{_bindir}
done
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -r $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc admin/%{name}-%{version}/package/COPYING
%doc admin/%{name}-%{version}/doc/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man8/*
#%{_mandir}/man1/*
