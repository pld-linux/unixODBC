Summary:	unixODBC
Summary(pl):	unixODBC
Name:		unixODBC
Version:	1.8.6	
Release:	1
License:	LGPL
Group:		Libraries
Group(pl):	Biblioteki
Source0:	ftp://ftp.easysoft.com/pub/beta/%{name}/%{name}-%{version}.tar.gz
Patch0:		unixODBC-DESTDIR.patch
#BuildRequires:	XFree86-devel
#BuildRequires:	qt-devel >= 2.0
Buildroot:	/tmp/%{name}-%{version}-root

%define		_prefix		/usr
%define		_sysconfdir	/etc

%description


%description -l pl


%package devel
Summary:	unixODBC
Summary(pl):	unixODBC
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki

%description devel


%description -l pl devel


%package static
Summary:	unixODBC
Summary(pl):	unixODBC
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki

%description static


%description -l pl static


%prep
%setup -q 
%patch -p1

%build
libtoolize --force
automake
LDFLAGS="-s"; export LDFLAGS
%configure \
	--disable-gui \
	--enable-threads \
	--enable-drivers \
	--enable-shared \
	--enable-static 
# GUI requires QT2	
#	--enable-gui 
#	--with-qt-dir=%{_prefix} 
make 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

gzip -9fn AUTHORS NEWS

find doc -name Makefile\* -exec rm {} \;

%post -p ldconfig
%postun -p ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,NEWS}.gz doc/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 size mtime)  %{_sysconfdir}/odbc*.ini

%files devel
#doc {AUTHORS,NEWS}.gz doc/*
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%attr(644,root,root) 
%{_libdir}/lib*.a
