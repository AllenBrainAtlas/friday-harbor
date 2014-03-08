function WriteVolume( M, fname, format )

if nargin < 3, format = 'float32'; end

fid = fopen( fname, 'w', 'l' );
if  fid == -1
    return;
end

fwrite( fid, M, format );
fclose( fid );