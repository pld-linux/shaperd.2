Summary:	Shaperd - bandwidth limiting
Summary(pl):	Shaperd - dzielenie ³±cza
Name:		shaperd.2
Version:	2.42
Release:	0.1
License:	GPL
Group:		Networking/Admin
#Source0:	http://sp9wun.republika.pl/prg/%{name}.%{version}.tar.gz
# Changed source to decrease traffic at republika.pl
Source0:	http://www.cbq.trzepak.net/prg/%{name}.%{version}.tar.gz
# Source0-md5:	87191c7772f92ae78bcaa49667de4496
Source1:	%{name}.init
Source2:	%{name}.conf
Patch0:		%{name}-fhs.patch
Patch1:		%{name}-iptables_path.patch
#URL:		http://sp9wun.republika.pl/linux/shaperd_cbq.html
URL:		http://www.cbq.trzepak.net/linux/shaperd_cbq.html
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	firewall-userspace-tool
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir		%{_datadir}/%{name}
%define		_sysconfdir	/etc/shaper
%define		_initrddir	/etc/rc.d/init.d
%define		_apache1dir	/etc/apache
%define		_apache2dir	/etc/httpd

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
Requires:	%{name} = %{version}-%{release}
Requires:	php
Requires:	webserver

%description php
PHP script for shaperd.

%description php -l pl
Skrypt PHP dla shaperd.

%prep
%setup -q -n shaperd
%patch0 -p1
%patch1 -p1

%build
%{__make} clean
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_initrddir},/var/lib/shaper,%{_phpdir},/etc/httpd}

install src/shaperd $RPM_BUILD_ROOT%{_sbindir}
install scripts/kto-daemon $RPM_BUILD_ROOT%{_sbindir}
install config/* $RPM_BUILD_ROOT%{_sysconfdir}
install scripts/kto.php $RPM_BUILD_ROOT%{_phpdir}/shaperd.php
install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/shaperd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add shaperd
%service shaperd restart "shaperd daemon"

%preun
if [ "$1" = "0" ]; then
	%service shaperd stop
	/sbin/chkconfig --del shaperd
fi

%post php
# apache1
if [ -d %{_apache1dir}/conf.d ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache1dir}/conf.d/99_%{name}.conf
	%service -q apache restart
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
	%service -q httpd restart
fi

%preun php
if [ "$1" = "0" ]; then
	# apache1
	if [ -d %{_apache1dir}/conf.d ]; then
		rm -f %{_apache1dir}/conf.d/99_%{name}.conf
		%service -q apache reload
	fi
	# apache2
	if [ -d %{_apache2dir}/httpd.conf ]; then
		rm -f %{_apache2dir}/httpd.conf/99_%{name}.conf
		%service -q httpd reload
	fi
fi

%files
%defattr(644,root,root,755)
%doc doc/shaperd_cbq.html
%doc doc/shaperd_cbq_en.html
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/[iqs]*
%attr(755,root,root) %{_sbindir}/shaperd
%attr(754,root,root) %{_initrddir}/shaperd
%dir /var/lib/shaper

%files php
%defattr(644,root,root,755)
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache-%{name}.conf
%dir %{_phpdir}
%attr(755,root,root) %{_sbindir}/kto-daemon
%{_phpdir}/shaperd.php
