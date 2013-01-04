(require 'color-theme)
(color-theme-initialize)
(color-theme-clarity)
(scroll-bar-mode -1)
(menu-bar-mode -1)
(tool-bar-mode -1)
(set-default-font "Inconsolata")
(setq inhibit-splash-screen t)

(setq TeX-PDF-mode t)

;;use evince instead of xpdf which seg faults!
(setq TeX-view-program-list '(("Evince" "evince --page-index=%(outpage) %o")))
(setq TeX-view-program-selection '((output-pdf "Evince")))

(add-hook 'LaTeX-mode-hook 'TeX-source-correlate-mode)
(setq TeX-source-correlate-start-server t)


;;SPELLCHECK
(setq ispell-program-name "aspell") 
    ; could be ispell as well, depending on your preferences 
(setq ispell-dictionary "english") 
    ; this can obviously be set to any language your spell-checking program supports

(add-hook 'LaTeX-mode-hook 'flyspell-mode) 
(add-hook 'LaTeX-mode-hook 'flyspell-buffer)
;;SPELLCHECK



 ;;(set-frame-parameter (selected-frame) 'alpha '(<active> [<inactive>]))
 (set-frame-parameter (selected-frame) 'alpha '(85 50))
 (add-to-list 'default-frame-alist '(alpha 85 50))

;;(set-frame-parameter (selected-frame) 'alpha '(<active> [<inactive>]))  
(set-frame-parameter (selected-frame) 'alpha '(85 50))  
(add-to-list 'default-frame-alist '(alpha 85 50))

(eval-when-compile (require 'cl))  
(defun toggle-transparency ()  
(interactive)  
(if (/= 
    (cadr (find 'alpha (frame-parameters nil) :key #'car)) 
    100)  
   (set-frame-parameter nil 'alpha '(100 100))
 (set-frame-parameter nil 'alpha '(85 60))))  
 (global-set-key (kbd "C-c s") 'toggle-transparency)

 (defun transparency (value)
   "Sets the transparency of the frame window. 0=transparent/100=opaque"
   (interactive "nTransparency Value 0 - 100 opaque:")
   (set-frame-parameter (selected-frame) 'alpha value))

(global-set-key [(f8)] 'loop-alpha)

(defvar alpha-list '((100 100) (95 65) (85 55) (75 45) (65 35)))

(defun next-alpha ()
  (let ((current-alpha
         (or (frame-parameter (selected-frame) 'alpha)
             (first alpha-list)))
        (lst alpha-list))
    (or (second
         (catch 'alpha
           (while lst
             (when (equal (first lst) current-alpha)
               (throw 'alpha lst))
             (setf lst (cdr lst)))))
        (first alpha-list))))

(defun loop-alpha ()
  (interactive)
  (let ((new-alpha (next-alpha))
        (current-default (assoc 'alpha default-frame-alist)))
    (set-frame-parameter (selected-frame) 'alpha new-alpha)
    (if current-default
        (setcdr current-default new-alpha)
      (add-to-list 'default-frame-alist (cons 'alpha new-alpha)))))

(load "~/nxhtml/nxhtml/autostart")

