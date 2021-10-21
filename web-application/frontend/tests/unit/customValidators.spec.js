import { 
  containsUppercase,
  containsLowercase,
  containsNumber,
  containsSpecial,
} from '../../src/helpers/customValidators'


describe('containsUppercase', () => {
  it('should return true if input contains uppercase character', () => {
    const goodInput = 'Abcdef';
    expect(containsUppercase(goodInput)).toBeTruthy();
  });
  it('should return false if input does not contain uppercase character', () => {
    const badInput = 'abcdef';
    expect(containsUppercase(badInput)).not.toBeTruthy();
  });
});

describe('containsLowercase', () => {
  it('should return true if input contains lowercase character', () => {
    const goodInput = 'abcdef';
    expect(containsLowercase(goodInput)).toBeTruthy();
  });
  it('should return false if input does not contain lowercase character', () => {
    const badInput = 'ABCDEF';
    expect(containsLowercase(badInput)).not.toBeTruthy();
  });
});

describe('containsNumber', () => {
  it('should return true if input contains number', () => {
    const goodInput = 'abcdef111';
    expect(containsNumber(goodInput)).toBeTruthy();
  });
  it('should return false if input does not contain number', () => {
    const badInput = 'abcdef';
    expect(containsNumber(badInput)).not.toBeTruthy();
  });
});

describe('containsSpecial', () => {
  it('should return true if input contains number', () => {
    const goodInput = 'abcdef!@#';
    expect(containsSpecial(goodInput)).toBeTruthy();
  });
  it('should return false if input does not contain number', () => {
    const badInput = 'abcdef';
    expect(containsSpecial(badInput)).not.toBeTruthy();
  });
});
