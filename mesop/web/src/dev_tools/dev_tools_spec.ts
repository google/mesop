import {waitForAsync, TestBed} from '@angular/core/testing';
import {DevTools} from './dev_tools';

describe('Dev Tools', () => {
  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({imports: [DevTools]});
  }));

  it('should bootstrap', () => {
    const fixture = TestBed.createComponent(DevTools);
    expect(fixture).toBeTruthy();
  });
});
