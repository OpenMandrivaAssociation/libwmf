%define api 0.2
%define major 7
%define libname %mklibname wmf %{api} %{major}
%define litename %mklibname wmflite %{api} %{major}
%define devname %mklibname -d wmf

%define _disable_rebuild_configure %nil

Summary:	A library to convert wmf files
Name:		libwmf
Version:	0.2.12
Release:	1
License:	GPLv2
Group:		Text tools
Url:		https://github.com/caolanm/libwmf
Source0:	https://github.com/caolanm/libwmf/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(libxml-2.0)

Requires(post,postun):	gdk-pixbuf2.0
Requires:	urw-fonts

%description
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

%files
%license COPYING
%{_bindir}/wmf2*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/io-wmf.*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	A library to convert wmf files. - library files
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libwmf.

%files -n %{libname}
%{_libdir}/libwmf-%{api}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{litename}
Summary:	A library to convert wmf files. - library files
Group:		System/Libraries
Conflicts:	%{libname} < 0.2.8.4-26

%description -n %{litename}
This package contains the library needed to run programs dynamically
linked with libwmflite.

%files -n %{litename}
%{_libdir}/libwmflite-%{api}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	A library to convert wmf files. - development environment
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libwmf-devel = %{version}-%{release}

%description -n %{devname}
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

Install libwmf-devel if you need to compile an application with libwmf
support.

%files -n %{devname}
%doc CREDITS README NEWS ChangeLog
%{_bindir}/libwmf-config
%{_libdir}/libwmf.so
%{_libdir}/libwmflite.so
%{_includedir}/libwmf
%{_libdir}/pkgconfig/%{name}.pc

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
autoreconf -i -f -Ipatches
%configure \
	--with-libxml2 \
	--disable-static

%make_build

%install
%make_install
rm -rf $RPM_BUILD_ROOT%{_includedir}/libwmf/gd
find doc -name "Makefile*" -exec rm {} \;
#we're carrying around duplicate fonts
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*afm
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*t1
sed -i $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/fontmap -e 's#libwmf/fonts#fonts/urw-base35#g'
# remove anything relevant to fonts.
rm -rf %{buildroot}%{_bindir}/libwmf-fontmap %{buildroot}%{_datadir}/libwmf
