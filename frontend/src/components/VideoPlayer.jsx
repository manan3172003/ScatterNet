import { forwardRef, useEffect, useRef, useState, useImperativeHandle } from 'react';
import React from 'react';

/**
 * https://imagekit.io/blog/react-video-player/
 */
const VideoPlayer = forwardRef(({ 
  src, 
  onPlay, 
  onEnded, 
  className = "reel-video",
  controls = true,
  autoPlay = true,
  muted = false,
}, ref) => {
  const videoRef = useRef(null);  
  const [isLoading, setIsLoading] = useState(true);
  useImperativeHandle(ref, () => ({
    ...videoRef.current,
    play: () => videoRef.current?.play(),
    pause: () => videoRef.current?.pause(),
    load: () => videoRef.current?.load(),
    get currentTime() { return videoRef.current?.currentTime},
    set currentTime(value) { 
      if (videoRef.current) videoRef.current.currentTime = value 
    },
    get duration() { return videoRef.current?.duration},
    get paused() { return videoRef.current?.paused},
    get ended() { return videoRef.current?.ended},
    seekTo: (time) => {
      if (videoRef.current) {
        videoRef.current.currentTime = time;
      }
    }
  }));
  
  // Setting up the event listeners when component mounts
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    // Defining the various event handlers for the video
    const handlers = {
      loadstart: () => setIsLoading(true),
      canplay: () => setIsLoading(false),
      
      // Playback events
      play: (e) => {
        if (onPlay) onPlay(e);
      },
      ended: (e) => {
        if (onEnded) onEnded(e);
      },
      // Video Error Events
      error: (e) => {
        const errorCode = video.error ? video.error.code : 'unknown';
        console.error(`Video error (${errorCode})`, e);
        setIsLoading(false);
      }
    };
    
    // Attaching event listeners to the video
    Object.entries(handlers).forEach(([event, handler]) => {
      if (handler) {
        video.addEventListener(event, handler);
      }
    });
    
    // Removeing event listeners when the component unmounts
    return () => {
      Object.entries(handlers).forEach(([event, handler]) => {
        if (handler) {
          video.removeEventListener(event, handler);
        }
      });
    };
  }, [onPlay, onEnded]);
  
  useEffect(() => {
    const video = videoRef.current;
    if (!video || !src) return;
    
    setIsLoading(true);
    video.pause();
    video.currentTime = 0;
    video.src = src;
    video.load();
    
    if (autoPlay) {
      const playPromise = video.play();
      if (playPromise !== undefined) {
        playPromise.catch(err => {
          if (err.name === 'NotAllowedError' && !muted) {
            video.muted = true;
            video.play().catch(() => {});
          }
        });
      }
    }
  }, [src, autoPlay, muted]);
  
  return (
    <div className="video-player-wrapper" style={{ position: 'relative' }}>
      <video
        ref={videoRef}
        src={src}
        controls={controls}
        autoPlay={autoPlay}
        muted={muted}
        playsInline
        preload="auto"
        className={className}
        style={{ width: '100%' }}
      />
      {isLoading && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: 'rgba(243, 238, 238, 0.5)',
          borderRadius: '50%',
          width: '60px',
          height: '60px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontSize: '12px'
        }}>
          Loading...
        </div>
      )}
    </div>
  );
});

export default VideoPlayer;