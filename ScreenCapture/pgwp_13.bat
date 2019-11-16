@echo off

cl -Zi -W3 -nologo^
   ../aissac.cpp^
   Dxgi.lib D3D11.lib user32.lib gdi32.lib shell32.lib Shcore.lib^
   -LD /link^
   /EXPORT:get_image^
   /EXPORT:init^
   /EXPORT:get_capture_height^
   /EXPORT:get_capture_width^
   /EXPORT:get_capture_num_components^
   /EXPORT:capture_frame^
   /EXPORT:list_processes || goto :error

goto :EOF

:error
popd
exit /b %errorlevel%
