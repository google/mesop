import {waitForAsync, TestBed} from '@angular/core/testing';
import {DevTools} from './dev_tools';
import {TEST_ONLY} from '../editor/editor';
import {EditorService} from '../services/editor_service';

const {EditorServiceImpl} = TEST_ONLY;

describe('Dev Tools', () => {
  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [DevTools],
      providers: [{provide: EditorService, useClass: EditorServiceImpl}],
    });
  }));

  it('should bootstrap', () => {
    const fixture = TestBed.createComponent(DevTools);
    expect(fixture).toBeTruthy();
  });
});
