function M = ReadVolume( fname, format, mydim )

global dimSize

if nargin < 2, format = 'float32'; end
if nargin < 3, mydim = dimSize; end

count = prod(mydim);

fid = fopen( fname, 'r', 'l' );
if fid == -1
    M = [];
    return;
end

M = fread( fid, count, format );
fclose( fid );