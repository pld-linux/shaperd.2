Summary:	Shaperd - bandwidth limiting
Summary(pl):	Shaperd - dzielenie ³±cza
Name:		shaperd.2
Version:	2.11
Release:	2
License:	GPL
Group:		Networking/Admin
#Source0:	http://sp9wun.republika.pl/prg/%{name}.%{version}.tar.gz
# Changed source to decrease traffic at republika.pl
Source0:	http://www.cbq.trzepak.net/prg/%{name}.%{version}.tar.gz
# Source0-md5:	b9b8de9c3b83668cd50b7b63e0d3ff56
Source1:	%{name}.init
Patch0:		%{name}-fhs.patch
Patch1:		%{name}-iptables_path.patch
#URL:		http://sp9wun.republika.pl/linux/shaperd_cbq.html
URL:		http://www.cbq.trzepak.net/linux/shaperd_cbq.html
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir		/home/services/httpd/html

%description
This program limits bandwidth on the ethernet/ppp interface and
divides it between the hosts in the local network.

%description -l pl
Program potrafi ograniczaæ przepustowo¶æ interfejsu ethernet/ppp oraz
dzieliæ dostêpne pasmo pomiêdzy komputery w sieci lokalnej.

%package php
Summary:	PHP script for shaperd
Summary(pl):	Skrypt PHP dla shaperd
Group:		Networking/Admin
Requires:	%{name} = %{version}
Requires:	php
Requires:	webserver

%description php
PHP script for Shaperd.

%description php -l pl
Skrypt PHP dla Shaperd-a.

%prep
%setup -q -n shaperd
%patch0 -p1
%patch1 -p1

%build
%{__make} clean
# this file has its own rule in Makefile, without CFLAGS...
%{__cc} %{rpmcflags} -c shaperd_old.c
%{__make} \
	CC=%{__cc} \
	CFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/shaper,%{_initrddir},/var/lib/shaper,%{_phpdir}}

install shaperd $RPM_BUILD_ROOT%{_sbindir}
install etc/shaper/* $RPM_BUILD_ROOT%{_sysconfdir}/shaper
install var/www/html/kto.php $RPM_BUILD_ROOT%{_phpdir}/shaperd.php
install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/shaperd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add shaperd
if [ -f /var/lock/subsys/shaperd ]; then
	/etc/rc.d/init.d/shaperd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/shaperd start\" to start shaperd daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/shaperd ]; then
		/etc/rc.d/init.d/shaperd stop >&2
	fi
	/sbin/chkconfig --del shaperd
fi

%files
%defattr(644,root,root,755)
%doc changes.txt kto-daemon usr/share/docs/shaperd-2.2.11/shaperd_cbq.html
%dir %{_sysconfdir}/shaper
%attr(640,root,root) %verify(not size md5 mtime) %config(noreplace) %{_sysconfdir}/shaper/*
%attr(755,root,root) %{_sbindir}/shaperd
%attr(754,root,root) %{_initrddir}/shaperd
%dir /var/lib/shaper

%files php
%defattr(644,root,root,755)
%attr(644,root,root) %{_phpdir}/shaperd.php
