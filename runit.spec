Summary:	A UNIX init scheme with service supervision
Summary(pl.UTF-8):	Implementacja uniksowego inita z dozorem usług
Name:		runit
Version:	2.0.0
Release:	0.1
License:	BSD style
Group:		Daemons
Source0:	http://smarden.org/runit/%{name}-%{version}.tar.gz
# Source0-md5:	63c53d313736f444a53a7451bfa76991
Patch0:		%{name}-nostatic.patch
Source1:	http://fisheye1.cenqua.com/browse/~raw,r=1.1/smeserver/runit/S/%{name}.svup
Source2:	http://fisheye1.cenqua.com/browse/~raw,r=1.1/smeserver/runit/S/%{name}.svdown
Source3:	http://fisheye1.cenqua.com/browse/~raw,r=1.1/smeserver/runit/S/%{name}.svdepcalc
Source4:	http://fisheye1.cenqua.com/browse/~raw,r=1.1/smeserver/runit/S/%{name}.dependencies.README
URL:		http://smarden.org/runit/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
runit is a daemontools alike replacement for SysVinit and other init
schemes. runit runs on GNU/Linux, OpenBSD, FreeBSD, and can easily be
adapted to other Unix operating systems.

Warning: Replacing SysVinit or init can cause the system's boot to
fail. Make sure you are able to recover and repair your system, for
example if you run a boot loader, it should be able to pass
init=/bin/sh to the kernel.

%description -l pl.UTF-8
runit to podobny do daemontools zamiennik demona SysVinit i innych
rodzajów procesu init. Działa na systemach GNU/Linux, OpenBSD
i FreeBSD, może być łatwo zaadaptowany do innych systemów uniksowych.

Uwaga: podmiana pakietu SysVinit lub innego inita może spowodować, że
system nie będzie mógł się uruchomić. Należy się upewnić, że jest
możliwość odtworzenia i naprawy systemu, na przykład z poziomu
bootloadera przez przekazanie do jądra init=/bin/sh.

%prep
%setup -qc
mv admin/%{name}-%{version}/* .
%patch0 -p1
cp -a %{SOURCE4} doc/dependencies.README
rm -f doc/debian

%build
echo '%{__cc} %{rpmldflags}' > src/conf-ld
echo '%{__cc} %{rpmcflags} -Wall' > src/conf-cc
./package/compile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
for i in $(cat package/commands); do
	install command/$i $RPM_BUILD_ROOT%{_sbindir}
done
install %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/svisup
install %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}/svisdown
install %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}/svdepcalc
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
