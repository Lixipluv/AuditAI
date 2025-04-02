<script>
    let modalOpen = false;
  </script>
  
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Lato', sans-serif;
    }
  
    body {
      color: #1f4568;
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center;
    }
  
    .sect {
      padding: 90px 0;
      position: relative;
      text-align: center;
    }
  
    .btn {
      display: inline-block;
      padding: 10px 25px;
      border-radius: 20px;
      background-color: #3a9fff;
      color: #fff;
      text-decoration: none;
      transition: 0.3s;
      margin: 10px;
    }
  
    .btn:hover {
      background-color: #63b2fc;
    }
  
    .btn--revert {
      background: transparent;
      color: #8198ae;
      border: 1px solid #c9d9e9;
    }
  
    .btn--revert:hover {
      color: #1f4568;
      border-color: #8198ae;
    }
  
    .modal-container {
      position: fixed;
      top: 0;
      left: 0;
      z-index: 10;
      display: flex;
      justify-content: center;
      align-items: center;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.6);
      visibility: hidden;
      opacity: 0;
      transition: visibility 0.3s, opacity 0.3s;
    }
  
    .modal-container.show {
      visibility: visible;
      opacity: 1;
    }
  
    .modal {
      width: 50rem;
      padding: 3rem;
      border-radius: 0.8rem;
      background: #fff;
      box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
      text-align: center;
      position: relative;
    }
  
    .modal__btn {
      padding: 1rem 2rem;
      border-radius: 5px;
      background-color: #1885ed;
      color: white;
      text-decoration: none;
      transition: 0.3s;
    }
  
    .modal__btn:hover {
      background-color: #1261a0;
    }
  
    .close {
      position: absolute;
      top: 1rem;
      right: 1rem;
      font-size: 2rem;
      text-decoration: none;
      color: #333;
      cursor: pointer;
    }
  
    .close:hover {
      color: #000;
    }
  </style>
  
  <div class="sect" style="text-align: center; padding: 40px 20px;">
    <h1 style="margin-bottom: 10px;">🚀 Welcome to <span style="color:#3C91E6;">AuditAI</span> 🔍</h1>
    <h2 style="margin-bottom: 15px;">📊 Generate Comprehensive Reports with Precision</h2>
    <p style="font-size: 18px; color: #555; margin-bottom: 25px;">
        🔐 Enhance security, 🤖 automate analysis, and 🏆 audit like a pro.
    </p>
    <div>
      <a class="btn" href="">Start</a>
      <button class="btn btn--revert" on:click={() => modalOpen = true}>GitHub</button>
    </div>
    <img src="https://image.ibb.co/c7grYb/image3015.png" alt="Smart Read">
  </div>
  
<!-- Modal -->
<div class="modal-container {modalOpen ? 'show' : ''}">
  <div class="modal">
      <h1 style="display: flex; align-items: center; gap: 10px; padding: 20px 0;">
          📂 GitHub Repository
      </h1>
      <p style="padding: 20px"> Check out our project on GitHub and explore its full potential.</p>
      <p style="padding: 20px"> Contribute to the development, review the source code, and stay updated with the latest features.</p>
      
      <a href="https://github.com/Lixipluv/AuditAI" target="_blank" class="modal__btn"
         style="display: inline-block; padding: 12px 20px; background-color: #3C91E6; 
                color: white; font-size: 16px; border-radius: 5px; text-decoration: none; 
                font-weight: bold; transition: 0.3s;">
          🔗 Visit GitHub →
      </a>
      
      <span class="close" on:click={() => modalOpen = false} 
            style="position: absolute; top: 15px; right: 20px; font-size: 24px; 
                   cursor: pointer; color: #888; transition: 0.3s;">
          ✖️
      </span>
  </div>
</div>