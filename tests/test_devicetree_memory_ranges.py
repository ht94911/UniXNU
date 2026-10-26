"""Exercise preserved DRAM holes and reject unsafe input ranges."""
import shutil,struct,subprocess,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from unixnu import devicetree as dt
@unittest.skipUnless(shutil.which('dtc'),'dtc required')
class MemoryRanges(unittest.TestCase):
 def make(self,root,banks):
  source='/dts-v1/; / { #address-cells=<2>;#size-cells=<2>; model="test"; compatible="test,board";cpus {#address-cells=<1>;#size-cells=<0>;timebase-frequency=<19200000>;cpu@0 {device_type="cpu";compatible="arm,cortex-a55";reg=<0>;};};'
  for base,size in banks:source+=f'memory@{base:x} {{device_type="memory";reg=<0x{base>>32:x} 0x{base&0xffffffff:x} 0x{size>>32:x} 0x{size&0xffffffff:x}>;}};'
  source+='};';s=root/'input.dts';o=root/'input.dtb';s.write_text(source);subprocess.run(['dtc','-I','dts','-O','dtb','-o',o,s],check=True,capture_output=True);return o
 def test_holes_preserved_only_on_explicit_opt_in(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);banks=[(0x80000000,0x10000000),(0xc0000000,0x20000000)];f=self.make(root,banks)
   with self.assertRaises(dt.Error):dt.generate(f,{})
   result=dt.generate(f,{'device_tree':{'preserve_memory_ranges':True}})
   pairs=struct.pack('<4Q',0x80000000,0x10000000,0xc0000000,0x20000000)
   self.assertIn(pairs,result);self.assertNotIn(struct.pack('<2Q',0x80000000,0x60000000),result)
 def test_missing_zero_overlap_and_overflow_rejected(self):
  for banks in [[],[(0x80000000,0)],[(0x80000000,0x20000000),(0x90000000,0x20000000)],[(0xfffffffffffff000,0x2000)]]:
   with self.subTest(banks=banks),tempfile.TemporaryDirectory() as tmp:
    with self.assertRaises(dt.Error):dt.generate(self.make(Path(tmp),banks),{'device_tree':{'preserve_memory_ranges':True}})
if __name__=='__main__':unittest.main()
